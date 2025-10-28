
import os
from playwright.sync_api import sync_playwright, expect

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Go to the local HTML file - this is needed to set the origin for localStorage
        page.goto('file://' + os.path.abspath('index.html'))

        # Simulate a logged-in user
        page.evaluate("""() => {
            localStorage.setItem('isLoggedIn', 'true');
            localStorage.setItem('currentUser', JSON.stringify({
                id: 'test',
                email: 'test@example.com',
                name: 'Test User'
            }));
        }""")

        # Reload the page for the changes to take effect
        page.reload()

        # Open the settings modal
        page.click('#settingsBtn')

        # Wait for the modal to appear and assert it's visible
        modal = page.locator('#settingsModal')
        expect(modal).to_be_visible()

        # Take a screenshot of the restructured modal
        page.screenshot(path='jules-scratch/verification/settings_modal.png')

        # Test changing the user icon color
        new_color = '#ff0000'
        page.fill('#userIconColorInput', new_color)
        page.click('#settingsSave')

        # Assert that the icon color has changed
        user_icon = page.locator('#userIconContainer')
        expect(user_icon).to_have_css('background-color', 'rgb(255, 0, 0)')

        # Re-open the settings modal to test the other features
        page.click('#settingsBtn')
        expect(modal).to_be_visible()

        # Test changing the display name
        page.once('dialog', lambda dialog: dialog.accept(prompt_text='New Name'))
        page.click('#changeDisplayNameBtn')

        # Assert that the name has been updated
        name_element = page.locator('h1.text-base.font-medium.leading-normal')
        expect(name_element).to_have_text('New Name')

        # Close the settings modal before deleting the account
        page.click('#settingsCancel')
        expect(modal).to_be_hidden()

        # Re-open the settings modal to delete account
        page.click('#settingsBtn')
        expect(modal).to_be_visible()

        # Test deleting the account
        page.once('dialog', lambda dialog: dialog.accept())
        page.click('#deleteAccountBtn')

        # Assert that the user is logged out and the login popup is visible
        login_popup = page.locator('#loginPopup')
        expect(login_popup).to_be_visible()

        browser.close()

if __name__ == '__main__':
    run()
