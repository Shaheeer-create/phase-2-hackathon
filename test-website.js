import { chromium, Page } from 'playwright';
import { execSync } from 'child_process';
import * as fs from 'fs';

async function runPlaywrightTest() {
  // Launch the browser
  const browser = await chromium.launch({ headless: false }); // Set to true to run headless
  const page = await browser.newPage();

  try {
    // Visit the frontend homepage
    console.log('Navigating to the Todo App homepage...');
    await page.goto('http://localhost:3000');

    // Wait for the page to load
    await page.waitForSelector('text=Todo App');
    console.log('Successfully loaded the homepage');

    // Take a screenshot
    await page.screenshot({ path: 'homepage.png' });
    console.log('Screenshot saved as homepage.png');

    // Check if we're redirected to signup (which is expected)
    const currentUrl = page.url();
    console.log(`Current URL: ${currentUrl}`);
    
    if (currentUrl.includes('/signup')) {
      console.log('Successfully redirected to signup page');
      
      // Fill in the signup form
      await page.fill('input[type="email"]', 'playwright-test@example.com');
      await page.fill('input[name="username"]', 'playwright-test');
      await page.fill('input[type="password"]', 'SecurePass123!');
      
      // Take screenshot before submitting
      await page.screenshot({ path: 'filled-signup.png' });
      console.log('Filled signup form, screenshot saved as filled-signup.png');
      
      // Submit the form
      await page.click('button[type="submit"]');
      console.log('Submitted signup form');
      
      // Wait for possible redirect to tasks page
      await page.waitForTimeout(3000); // Wait 3 seconds for any redirects
      
      const newUrl = page.url();
      console.log(`New URL after signup: ${newUrl}`);
      
      if (newUrl.includes('/tasks')) {
        console.log('Successfully navigated to tasks page after signup');
        await page.screenshot({ path: 'tasks-page.png' });
        console.log('Tasks page screenshot saved as tasks-page.png');
      } else {
        console.log('Did not navigate to tasks page, staying on current page');
        await page.screenshot({ path: 'post-signup.png' });
        console.log('Post-signup page screenshot saved as post-signup.png');
      }
    } else if (currentUrl.includes('/login')) {
      console.log('On login page instead of signup');
      await page.screenshot({ path: 'login-page.png' });
      console.log('Login page screenshot saved as login-page.png');
    } else {
      console.log('On an unexpected page after homepage load');
      await page.screenshot({ path: 'unexpected-page.png' });
      console.log('Unexpected page screenshot saved as unexpected-page.png');
    }

    // Visit the backend API root to confirm it's working
    console.log('Checking backend API...');
    const backendResponse = await page.goto('http://localhost:8000/');
    const backendText = await backendResponse.text();
    console.log('Backend response:', backendText);

  } catch (error) {
    console.error('Error during Playwright test:', error);
  } finally {
    // Close the browser
    await browser.close();
    console.log('Browser closed');
  }
}

// Run the test
runPlaywrightTest().catch(console.error);