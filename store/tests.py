from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product, Category, Order, OrderItem

class StoreCoreEngineeringTests(TestCase):
    
    def setUp(self):
        """Making a database for testig"""
        self.client = Client()
        
        ### Build relational category and product data keys
        self.category = Category.objects.create(name="Balloons")
        self.product = Product.objects.create(
            name="Giant Helium Balloon",
            price=4.99,
            category=self.category,
            image="uploads/product/test_balloon.jpg",
            stock=15
        )
        
        ### Create separate users to test permissions
        self.user_alice = User.objects.create_user(username="alice", password="securepassword123")
        self.user_bob = User.objects.create_user(username="bob", password="securepassword456")

    def test_homepage_view_status(self):
        """Check the store storefront landing page shows the products"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Giant Helium Balloon")



    def test_search_functionality(self):
        """Make sure search isn't case sensitive."""
        response = self.client.get(reverse('search'), {'q': 'helium'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Giant Helium Balloon")

    def test_order_history_requires_authentication(self):
        """Confirm that new users are blocked and redirected to login."""
        response = self.client.get(reverse('order_history'))
        self.assertEqual(response.status_code, 302)

    def test_order_isolation_permissions(self):
        """Security test to check  a user can only check their own records."""
        ### Create an order mapped directly to Alice
        alice_order = Order.objects.create(
            user=self.user_alice,
            full_name="Alice Smith",
            email="alice@test.com",
            shipping_address="123 Alice St",
            amount_paid=4.99

        )
        
        ### Try to log in as Bob 
        self.client.login(username="bob", password="securepassword456")
        response = self.client.get(reverse('order_history'))
        
        ### Bob's container MUST NOT leak Alice's record entries
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Alice Smith")
