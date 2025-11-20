
import { test, expect } from '@playwright/test';

test('has title', async ({ page }) => {
  await page.goto('http://localhost:3000/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/React App/);
});

test('login and upload statement', async ({ page }) => {
    await page.goto('http://localhost:3000/login');

    // Login
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('http://localhost:3000/dashboard');

    // Go to statements page
    await page.click('text=Statements');
    await expect(page).toHaveURL('http://localhost:3000/statements');

    // Upload a file
    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.click('text=Drag \'n\' drop some files here, or click to select files');
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles({
        name: 'test.csv',
        mimeType: 'text/csv',
        buffer: Buffer.from('col1,col2\nval1,val2'),
    });

    // Click the upload button
    await page.click('text=Upload and Process');

    // Wait for navigation
    await page.waitForURL('**/transactions/statement/**');

    // Check that the transactions are displayed
    await expect(page.locator('text=val1')).toBeVisible();
});
