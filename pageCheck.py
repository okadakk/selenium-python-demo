import csv
import re
import urllib.request

from pageTest import pageTest
from selenium.common.exceptions import TimeoutException

class pageCheck(pageTest):
    # 無視するコンソールエラーメッセージ。
    IGNORE_CONSOLE_ERRORS = [
        'https://image-dev',
        'chrome-extension://invalid/'
    ]

    def do_check_test(self):
        pattern = self._get_ignore_pattern()
        for urls in self._get_check_url_map():
            try:
                pc_url = urls[0]
                sp_url = urls[1]
                if len(urls) > 2:
                    print('URLにカンマが含まれている可能性があります。')
                    break
            except IndexError as e:
                print('CSVの形式が違います')
                break

            self._check_display_error(pc_url, pattern)
            self._check_display_error(sp_url, pattern)
            self._check_redirect_error(pc_url, sp_url)

        self._save_error_log()

        self.driver.close()
        self.mobile_driver.close()

    def _get_check_url_map(self):
        url_map = []
        # CSVの形式は [pcUrl, spUrl] のように対応するURLを1行ごとに記載してください。
        with open('csv/check_url_map.csv', 'r') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                url_map.append(row)
        return url_map

    def _get_ignore_pattern(self):
        return re.compile("|".join(self.IGNORE_CONSOLE_ERRORS))

    # 404, 500エラー、コンソールエラーを検知
    def _check_display_error(self, url, pattern):
        if url == '-':
            return

        # レスポンスコードを取得
        req = urllib.request.Request(url)
        try:
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            self._append_error_logs(url, 'HTTP Response Error ' + str(e.code))
            return

        # JSエラーを取得
        try:
            self._navigate_to_url(self.driver, url)
        except TimeoutException as e:
            self._append_error_logs(url, 'TimeoutException')
            return

        for entry in self.driver.get_log('browser'):
            message = entry['message']
            if re.search(pattern, message):
                continue
            self._append_error_logs(url, message)

        if self.driver.current_url != url:
            self._append_error_logs(url, 'Unexpectd Redirect Error')

    # リダイレクトチェック
    def _check_redirect_error(self, pc_url, sp_url):
        if pc_url == '-' or sp_url == '-':
            return

        try:
            self._navigate_to_url(self.mobile_driver, pc_url)
        except TimeoutException as e:
            self._append_error_logs(pc_url, 'Redirect TimeoutException')
            return

        if self.driver.current_url != sp_url:
            self._append_error_logs(pc_url, 'Redirect No Match Error')

pageCheck().do_check_test()
