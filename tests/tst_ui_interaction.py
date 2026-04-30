#tests/test_ui_interaction.py

from playwright.sync_api import sync_playwright, expect

def test_ui_interaction():

    #open
    with sync_playwright() as p:
        browser = p.chromium.launch(headless = False)
        page = browser.new_page()




    #click
        page.goto("https://www.dragracecentral.com")


    #locate and observe


        page.locator("[name='searchtext'][alt='search']").fill("Prather")#this is the search box

        page.get_by_role("button", name="send").click() #this is the "go>" button


    #assert
        expect(page.get_by_text("Searched: Prather")).to_be_visible()
        expect(page.get_by_text("Top Dragster Round 3")).to_be_visible()
        page.get_by_text("Top Dragster Round 3").click()
        locator = page.get_by_text("Prather")
        expect(locator.first).to_be_visible()
        #expect(page.get_by_text('Prather')).to_be_visible()
        browser.close()
