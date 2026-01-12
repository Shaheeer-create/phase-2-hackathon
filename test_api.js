// Simple test to verify the API is working
const axios = require('axios');

async function testApi() {
  try {
    console.log('Testing API connection...');
    
    // Test the registration endpoint
    const response = await axios.post('http://localhost:8000/api/auth/register', {
      email: 'testuser@example.com',
      password: 'password123',
      username: 'testuser'
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Registration successful:', response.data);
  } catch (error) {
    if (error.response) {
      console.log('API responded with error:', error.response.status, error.response.data);
    } else if (error.request) {
      console.log('Network error - no response received:', error.message);
    } else {
      console.log('Error setting up request:', error.message);
    }
  }
}

testApi();