#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Bot for displaying unfollowers for an Instagram account.


import os
import secrets
import selenium
import time

from selenium import webdriver


# ------------------------------------------------------------------------------
# Used for the Instagram login page
INSTAGRAM_LOGIN_URL = 'https://www.instagram.com/accounts/login/'
XPATH_LOGIN_NAME = '//input[@name="username"]'
XPATH_LOGIN_PASSWORD = '//input[@name="password"]'
XPATH_LOGIN_BUTTON = '//button[@type="submit"]'

# How long (in seconds) to wait for the login page to load.
LOGIN_PAGE_WAIT_TIME = 5

# How long (in seconds) to wait for the Instagram home feed to load.
IG_HOME_FEED_WAIT_TIME = 5

# Need to click on the button in order to conintue interacting with the home
# feed.
XPATH_TURN_OFF_NOTIFICATIONS_BUTTON = '//button[contains(text(), "Not Now")]'
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Used for going to a user's Instagram profile page which has their posts,
# followers, following, etc.
XPATH_PROFILE_PAGE = '//a[@href="/%s/"]' % secrets.username

# How long (in seconds) to wait for the user's profile page to fully load.
PROFILE_PAGE_WAIT_TIME = 3
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Used to operate on the 'following' tab on the user's profile page.
XPATH_FOLLOWING = '//a[@href="/%s/following/"]' % secrets.username
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Used to operate on the 'followers' tab on the user's profile page.
XPATH_FOLLOWERS = '//a[@href="/%s/followers/"]' % secrets.username
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Used for either the 'followers' or the 'following' tab in the user's profile
# page.

# How long (in seconds) to wait for the partial list in either the 'following'
# or the 'followers' tab to fully load (when scrolling through the entire
# list).
USER_CELL_LIST_WAIT_TIME = 1

# After clicking on the tab, a dialog box shows up which contains the list of
# all following users or all followers for the account.
XPATH_DIALOG_BOX = './/div[@role="dialog"]'

USER_CELL_TAG = 'li'

SCROLL = '/html/body/div[4]/div/div[2]'
SCROLL_SCRIPT = 'arguments[0].scrollTo(0, arguments[0].scrollHeight);' \
        'return arguments[0].scrollHeight;'
# ------------------------------------------------------------------------------


class InstagramBot:
    """A class with methods that operate on the Instagram bot."""
    def __init__(self, username, password):
        """Launches the Chrome browser and signs into the user's Instagram."""

        self.username = username
        self.password = password

        self.driver = webdriver.Chrome()

        # Load the Instagram login page.
        self.driver.get(INSTAGRAM_LOGIN_URL)

        time.sleep(LOGIN_PAGE_WAIT_TIME)

        # Login.
        self.driver.find_element_by_xpath(XPATH_LOGIN_NAME).send_keys(
                self.username)
        self.driver.find_element_by_xpath(XPATH_LOGIN_PASSWORD).send_keys(
                self.password)
        self.driver.find_element_by_xpath(XPATH_LOGIN_BUTTON).click()

        time.sleep(IG_HOME_FEED_WAIT_TIME)

        # A box might popup about enabling notifications in order to continue.
        try:
            self.driver.find_element_by_xpath(
                    XPATH_TURN_OFF_NOTIFICATIONS_BUTTON).click()
        except selenium.common.exceptions.NoSuchElementException:
            # No popup was found.
            pass

        # Successfully signed in and home feed has been loaded.

    def GoToInstagramProfilePage(self):
        """Goes to the user's profile page which shows their posts, etc."""

        self.driver.find_element_by_xpath(XPATH_PROFILE_PAGE).click()

        time.sleep(PROFILE_PAGE_WAIT_TIME)

    def OpenFollowingInstagramUsers(self):
        """Clicks on the 'following' tab that is in the user's profile page.

        This function assumes that the automated Chrome browser is currently on
        the user's Instagram home feed.

        """

        self.GoToInstagramProfilePage()

        self.driver.find_element_by_xpath(XPATH_FOLLOWING).click()

        time.sleep(USER_CELL_LIST_WAIT_TIME)

    def _CloseTab(self):
        """Closes the tab opened by clicking on 'following' or 'followers'."""

        dialog_box = self.driver.find_element_by_xpath(XPATH_DIALOG_BOX)

        dialog_box.find_element_by_tag_name('button').click()

    def GetFollowingInstagramUsers(self):
        """Returns a set of all Instagram user's that the user follows."""

        self.OpenFollowingInstagramUsers()

        following = self._ParseUserCells()

        self._CloseTab()

        return following

    def OpenInstagramFollowers(self):
        """Clicks on the 'followers' tab that is in the user's profile page.

        This function assumes that the automated Chrome browser is currently on
        the user's Instagram home feed.

        """

        self.GoToInstagramProfilePage()

        self.driver.find_element_by_xpath(XPATH_FOLLOWERS).click()

        time.sleep(USER_CELL_LIST_WAIT_TIME)

    def GetInstagramFollowers(self):
        """Returns a set of all Instagram followers that follow the user."""

        self.OpenInstagramFollowers()

        followers = self._ParseUserCells()

        self._CloseTab()

        return followers

    def _ParseUserCells(self):
        """Returns a set of a users (a set implies uniqueness).

        This function is called to either obtain all unique followers or all
        unique users that the user follows (e.g. following).
        """

        # Verify that there is at least 1 user cell.
        try:
            dialog_box = self.driver.find_element_by_xpath(XPATH_DIALOG_BOX)

            dialog_box.find_elements_by_tag_name(USER_CELL_TAG)
        except selenium.common.exceptions.NoSuchElementException:
            return {}

        scroll = self.driver.find_element_by_xpath(SCROLL)
        prev_height, cur_height = -1, 1

        # Find all users.
        while prev_height != cur_height:
            time.sleep(USER_CELL_LIST_WAIT_TIME)

            prev_height = cur_height
            cur_height = self.driver.execute_script(SCROLL_SCRIPT, scroll)

        a_tags = scroll.find_elements_by_tag_name('a')

        # Some elements with the 'a' tag have an empty string for `.text`
        # and those elements are not "users".
        return {user.text for user in a_tags if user.text != ''}

    def GetInstagramUnfollowers(self):
        """Returns a list of all Instagram unfollowers."""

        following_users = self.GetFollowingInstagramUsers()

        followers = self.GetInstagramFollowers()

        unfollowers = [user
                for user in following_users if user not in followers]

        self._PrintUnfollowers(unfollowers)

        return unfollowers

    def _PrintUnfollowers(self, unfollowers):
        """Prints all unfollowers for the account."""

        if not unfollowers:
            print('All Instagram users that you follow, follow you back!')
            return

        print('All unfollowers (their Instagram username):')
        for unfollower in unfollowers:
            print(unfollower)


def main():
    """Creates the IG bot and execs IG bot stuff."""

    if not secrets.username:
        raise ValueError('Please go to %s and add a `username`, where the '
            'value is a string and its your username for your Instagram '
            'account.' % os.path.abspath(secrets.__file__))
    elif not isinstance(secrets.username, str):
        raise ValueError('The value for `username` in %s is not a string, '
            'please make it.' % os.path.abspath(secrets.__file__))

    if not secrets.password:
        raise ValueError('Please go to %s and add a `password`, where the '
            'value is a string and its your password for your Instagram '
            'account.' % os.path.abspath(secrets.__file__))
    elif not isinstance(secrets.password, str):
        raise ValueError('The value for `password` in %s is not a string, '
            'please make it.' % os.path.abspath(secrets.__file__))

    IG_bot = InstagramBot(secrets.username, secrets.password)

    IG_bot.GetInstagramUnfollowers()

    IG_bot.driver.quit()


if __name__ == '__main__':
    main()
