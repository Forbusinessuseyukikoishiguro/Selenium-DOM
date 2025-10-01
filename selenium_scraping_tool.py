# ============================================
# Selenium スクレイピングサポートツール
# HTML/DOM構造を分析してスクレイピングをサポート
# ============================================

from selenium import webdriver  # Seleniumのメインモジュール
from selenium.webdriver.chrome.service import Service  # Chromeドライバー管理用
from selenium.webdriver.chrome.options import Options  # Chromeオプション設定用
from selenium.webdriver.common.by import By  # 要素検索方法の指定用
from selenium.webdriver.support.ui import WebDriverWait  # 待機処理用
from selenium.webdriver.support import expected_conditions as EC  # 待機条件用
from selenium.common.exceptions import TimeoutException, NoSuchElementException  # 例外処理用
import logging  # ログ出力用
from datetime import datetime  # 日時取得用
from typing import List, Dict, Optional  # 型ヒント用
import time  # 待機処理用
import json  # JSON出力用


# ============================================
# ログ設定
# ============================================

# ログ設定（ファイルとコンソール両方に出力）
logging.basicConfig(
    level=logging.DEBUG,  # DEBUGレベル以上を出力
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # ログフォーマット
    handlers=[
        logging.FileHandler('scraping.log', encoding='utf-8'),  # ファイルに保存
        logging.StreamHandler()  # コンソールにも表示
    ]
)

# ロガーを作成
logger = logging.getLogger(__name__)


# ============================================
# スクレイピングサポートクラス
# ============================================

class ScrapingSupport:
    """
    Webページの構造を分析してスクレイピングをサポートするクラス
    """
    
    def __init__(self, headless: bool = False):
        """
        初期化メソッド
        
        Args:
            headless: Trueの場合、ブラウザを非表示で実行
        """
        print("[DEBUG] ScrapingSupportクラスを初期化します")
        logger.info("ScrapingSupportクラスの初期化開始")
        
        self.driver = None  # Webドライバーを保存する変数
        self.headless = headless  # ヘッドレスモードのフラグ
        
        # Chromeオプションの設定
        self.options = Options()
        
        if self.headless:  # ヘッドレスモードの場合
            self.options.add_argument('--headless')  # ブラウザを表示しない
            print("[DEBUG] ヘッドレスモードを有効化")
            logger.debug("ヘッドレスモード有効")
        
        # その他の推奨オプション
        self.options.add_argument('--no-sandbox')  # サンドボックス無効化
        self.options.add_argument('--disable-dev-shm-usage')  # 共有メモリ使用を無効化
        self.options.add_argument('--disable-gpu')  # GPU使用を無効化
        self.options.add_argument('--window-size=1920,1080')  # ウィンドウサイズ指定
        self.options.add_argument('--lang=ja')  # 言語を日本語に設定
        
        # User-Agentを設定（ボット検出を回避）
        self.options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        print("[DEBUG] Chromeオプションの設定完了")
        logger.debug(f"Chromeオプション設定完了: headless={headless}")
    
    def start_driver(self):
        """Chromeドライバーを起動"""
        try:
            print("[DEBUG] Chromeドライバーを起動します")
            logger.info("Chromeドライバー起動開始")
            
            # Chromeドライバーを作成
            self.driver = webdriver.Chrome(options=self.options)
            
            # 暗黙的な待機時間を設定（要素が見つかるまで最大10秒待つ）
            self.driver.implicitly_wait(10)
            
            print("[DEBUG] ✅ Chromeドライバーの起動成功")
            logger.info("Chromeドライバー起動成功")
            return True
            
        except Exception as e:
            print(f"[DEBUG] ❌ Chromeドライバーの起動失敗: {e}")
            logger.error(f"Chromeドライバー起動失敗: {e}", exc_info=True)
            return False
    
    def open_url(self, url: str) -> bool:
        """
        指定されたURLを開く
        
        Args:
            url: アクセスするURL
            
        Returns:
            成功時True、失敗時False
        """
        try:
            print(f"[DEBUG] URLにアクセス: {url}")
            logger.info(f"URLアクセス開始: {url}")
            
            # URLを開く
            self.driver.get(url)
            
            # ページ読み込み完了を待つ
            time.sleep(2)
            
            # 現在のURLとタイトルを取得
            current_url = self.driver.current_url
            title = self.driver.title
            
            print(f"[DEBUG] ✅ ページ読み込み完了")
            print(f"[DEBUG] 現在のURL: {current_url}")
            print(f"[DEBUG] ページタイトル: {title}")
            
            logger.info(f"ページ読み込み成功: {title}")
            logger.debug(f"最終URL: {current_url}")
            
            return True
            
        except Exception as e:
            print(f"[DEBUG] ❌ URLアクセス失敗: {e}")
            logger.error(f"URLアクセス失敗: {url}, エラー: {e}", exc_info=True)
            return False
    
    def get_page_info(self) -> Dict[str, any]:
        """
        ページの基本情報を取得
        
        Returns:
            ページ情報の辞書
        """
        print("\n[DEBUG] ========== ページ基本情報 ==========")
        logger.info("ページ基本情報の取得開始")
        
        info = {
            'url': self.driver.current_url,  # 現在のURL
            'title': self.driver.title,  # ページタイトル
            'html_length': len(self.driver.page_source),  # HTML全体の長さ
        }
        
        # 情報を表示
        print(f"[DEBUG] URL: {info['url']}")
        print(f"[DEBUG] タイトル: {info['title']}")
        print(f"[DEBUG] HTML長: {info['html_length']:,} 文字")
        
        logger.info(f"ページ情報取得完了: {info['title']}")
        logger.debug(f"HTML長: {info['html_length']}")
        
        return info
    
    def analyze_dom_structure(self) -> Dict[str, any]:
        """
        DOM構造を分析
        
        Returns:
            DOM分析結果の辞書
        """
        print("\n[DEBUG] ========== DOM構造分析 ==========")
        logger.info("DOM構造分析開始")
        
        analysis = {}
        
        # 主要なHTML要素をカウント
        elements_to_count = [
            'div', 'span', 'p', 'a', 'img', 'table', 'tr', 'td',
            'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'form', 'input', 'button', 'select', 'textarea'
        ]
        
        print("[DEBUG] 要素数をカウント中...")
        
        for element in elements_to_count:
            try:
                # 要素を検索してカウント
                count = len(self.driver.find_elements(By.TAG_NAME, element))
                analysis[element] = count
                
                if count > 0:  # 存在する要素のみ表示
                    print(f"[DEBUG]   <{element}>: {count}個")
                    logger.debug(f"要素カウント: <{element}> = {count}")
                    
            except Exception as e:
                print(f"[DEBUG]   <{element}>: カウント失敗 ({e})")
                logger.warning(f"要素カウント失敗: <{element}>: {e}")
        
        logger.info("DOM構造分析完了")
        return analysis
    
    def find_elements_by_class(self, class_name: str) -> List:
        """
        クラス名で要素を検索
        
        Args:
            class_name: 検索するクラス名
            
        Returns:
            見つかった要素のリスト
        """
        print(f"\n[DEBUG] クラス名で検索: '{class_name}'")
        logger.info(f"クラス名検索: {class_name}")
        
        try:
            # クラス名で要素を検索
            elements = self.driver.find_elements(By.CLASS_NAME, class_name)
            
            print(f"[DEBUG] ✅ {len(elements)}個の要素が見つかりました")
            logger.info(f"クラス名検索成功: {len(elements)}個発見")
            
            # 各要素の情報を表示
            for i, element in enumerate(elements[:5], 1):  # 最初の5個のみ表示
                text = element.text[:50] if element.text else "(テキストなし)"
                print(f"[DEBUG]   [{i}] {text}...")
                logger.debug(f"要素[{i}]: {text[:30]}...")
            
            if len(elements) > 5:
                print(f"[DEBUG]   ... 他 {len(elements) - 5}個")
            
            return elements
            
        except Exception as e:
            print(f"[DEBUG] ❌ 検索失敗: {e}")
            logger.error(f"クラス名検索失敗: {class_name}, エラー: {e}")
            return []
    
    def find_elements_by_id(self, element_id: str):
        """
        IDで要素を検索
        
        Args:
            element_id: 検索する要素のID
            
        Returns:
            見つかった要素（単一）またはNone
        """
        print(f"\n[DEBUG] IDで検索: '{element_id}'")
        logger.info(f"ID検索: {element_id}")
        
        try:
            # IDで要素を検索（IDは一意なので単一要素）
            element = self.driver.find_element(By.ID, element_id)
            
            print(f"[DEBUG] ✅ 要素が見つかりました")
            print(f"[DEBUG]   タグ: {element.tag_name}")
            print(f"[DEBUG]   テキスト: {element.text[:100] if element.text else '(なし)'}...")
            
            logger.info(f"ID検索成功: {element_id}")
            logger.debug(f"要素タグ: {element.tag_name}")
            
            return element
            
        except NoSuchElementException:
            print(f"[DEBUG] ❌ 要素が見つかりません")
            logger.warning(f"ID検索失敗: {element_id} (要素なし)")
            return None
        except Exception as e:
            print(f"[DEBUG] ❌ 検索失敗: {e}")
            logger.error(f"ID検索エラー: {element_id}, エラー: {e}")
            return None
    
    def find_elements_by_tag(self, tag_name: str) -> List:
        """
        タグ名で要素を検索
        
        Args:
            tag_name: 検索するタグ名（例: 'a', 'img', 'div'）
            
        Returns:
            見つかった要素のリスト
        """
        print(f"\n[DEBUG] タグ名で検索: '<{tag_name}>'")
        logger.info(f"タグ検索: {tag_name}")
        
        try:
            # タグ名で要素を検索
            elements = self.driver.find_elements(By.TAG_NAME, tag_name)
            
            print(f"[DEBUG] ✅ {len(elements)}個の要素が見つかりました")
            logger.info(f"タグ検索成功: {len(elements)}個発見")
            
            return elements
            
        except Exception as e:
            print(f"[DEBUG] ❌ 検索失敗: {e}")
            logger.error(f"タグ検索失敗: {tag_name}, エラー: {e}")
            return []
    
    def find_all_links(self) -> List[Dict[str, str]]:
        """
        ページ内のすべてのリンクを取得
        
        Returns:
            リンク情報のリスト
        """
        print("\n[DEBUG] ========== リンク一覧 ==========")
        logger.info("リンク取得開始")
        
        try:
            # すべての<a>タグを検索
            links = self.driver.find_elements(By.TAG_NAME, 'a')
            
            link_data = []
            
            print(f"[DEBUG] {len(links)}個のリンクが見つかりました")
            logger.info(f"リンク数: {len(links)}")
            
            # 各リンクの情報を取得
            for i, link in enumerate(links[:10], 1):  # 最初の10個のみ表示
                href = link.get_attribute('href')  # href属性を取得
                text = link.text.strip()  # リンクテキストを取得
                
                if href:  # hrefが存在する場合のみ
                    link_info = {
                        'href': href,
                        'text': text if text else '(テキストなし)'
                    }
                    link_data.append(link_info)
                    
                    print(f"[DEBUG]   [{i}] {link_info['text'][:40]}")
                    print(f"[DEBUG]       → {href}")
                    logger.debug(f"リンク[{i}]: {text[:30]} -> {href}")
            
            if len(links) > 10:
                print(f"[DEBUG]   ... 他 {len(links) - 10}個")
            
            logger.info(f"リンク取得完了: {len(link_data)}個")
            return link_data
            
        except Exception as e:
            print(f"[DEBUG] ❌ リンク取得失敗: {e}")
            logger.error(f"リンク取得エラー: {e}")
            return []
    
    def find_all_images(self) -> List[Dict[str, str]]:
        """
        ページ内のすべての画像を取得
        
        Returns:
            画像情報のリスト
        """
        print("\n[DEBUG] ========== 画像一覧 ==========")
        logger.info("画像取得開始")
        
        try:
            # すべての<img>タグを検索
            images = self.driver.find_elements(By.TAG_NAME, 'img')
            
            image_data = []
            
            print(f"[DEBUG] {len(images)}個の画像が見つかりました")
            logger.info(f"画像数: {len(images)}")
            
            # 各画像の情報を取得
            for i, img in enumerate(images[:10], 1):  # 最初の10個のみ表示
                src = img.get_attribute('src')  # src属性を取得
                alt = img.get_attribute('alt')  # alt属性を取得
                
                if src:  # srcが存在する場合のみ
                    img_info = {
                        'src': src,
                        'alt': alt if alt else '(altなし)'
                    }
                    image_data.append(img_info)
                    
                    print(f"[DEBUG]   [{i}] alt='{img_info['alt'][:40]}'")
                    print(f"[DEBUG]       src: {src[:60]}...")
                    logger.debug(f"画像[{i}]: alt={alt} -> {src[:50]}")
            
            if len(images) > 10:
                print(f"[DEBUG]   ... 他 {len(images) - 10}個")
            
            logger.info(f"画像取得完了: {len(image_data)}個")
            return image_data
            
        except Exception as e:
            print(f"[DEBUG] ❌ 画像取得失敗: {e}")
            logger.error(f"画像取得エラー: {e}")
            return []
    
    def get_full_html(self, save_to_file: bool = True) -> str:
        """
        ページの完全なHTMLを取得
        
        Args:
            save_to_file: Trueの場合、ファイルに保存
            
        Returns:
            HTML文字列
        """
        print("\n[DEBUG] ========== HTML取得 ==========")
        logger.info("HTML取得開始")
        
        try:
            # ページのHTMLを取得
            html = self.driver.page_source
            
            print(f"[DEBUG] HTML長: {len(html):,} 文字")
            logger.info(f"HTML取得成功: {len(html)}文字")
            
            if save_to_file:
                # ファイル名を生成（タイムスタンプ付き）
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'scraped_html_{timestamp}.html'
                
                # ファイルに保存
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(html)
                
                print(f"[DEBUG] ✅ HTMLをファイルに保存: {filename}")
                logger.info(f"HTML保存完了: {filename}")
            
            return html
            
        except Exception as e:
            print(f"[DEBUG] ❌ HTML取得失敗: {e}")
            logger.error(f"HTML取得エラー: {e}")
            return ""
    
    def save_screenshot(self, filename: Optional[str] = None):
        """
        スクリーンショットを保存
        
        Args:
            filename: 保存するファイル名（省略時は自動生成）
        """
        print("\n[DEBUG] ========== スクリーンショット ==========")
        logger.info("スクリーンショット撮影開始")
        
        try:
            # ファイル名を生成
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f'screenshot_{timestamp}.png'
            
            # スクリーンショットを保存
            self.driver.save_screenshot(filename)
            
            print(f"[DEBUG] ✅ スクリーンショット保存: {filename}")
            logger.info(f"スクリーンショット保存完了: {filename}")
            
        except Exception as e:
            print(f"[DEBUG] ❌ スクリーンショット失敗: {e}")
            logger.error(f"スクリーンショットエラー: {e}")
    
    def generate_scraping_code(self, target_element: str) -> str:
        """
        スクレイピングコードのサンプルを生成
        
        Args:
            target_element: スクレイピング対象の要素（例: 'class_name', 'id', 'tag'）
            
        Returns:
            サンプルコード（文字列）
        """
        print("\n[DEBUG] ========== サンプルコード生成 ==========")
        logger.info(f"サンプルコード生成: {target_element}")
        
        code = f"""
# ===== Seleniumスクレイピングサンプルコード =====
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Chromeオプション設定
options = Options()
options.add_argument('--headless')  # ヘッドレスモード

# ドライバー起動
driver = webdriver.Chrome(options=options)

try:
    # URLを開く
    driver.get('{self.driver.current_url}')
    
    # 要素を取得（{target_element}の例）
    if '{target_element}' == 'class':
        elements = driver.find_elements(By.CLASS_NAME, 'your-class-name')
    elif '{target_element}' == 'id':
        element = driver.find_element(By.ID, 'your-element-id')
    elif '{target_element}' == 'tag':
        elements = driver.find_elements(By.TAG_NAME, 'div')
    
    # データ抽出
    for element in elements:
        text = element.text
        print(text)
    
finally:
    # ドライバー終了
    driver.quit()
"""
        
        print("[DEBUG] サンプルコード:")
        print(code)
        logger.debug("サンプルコード生成完了")
        
        return code
    
    def close(self):
        """ブラウザを閉じる"""
        if self.driver:
            print("\n[DEBUG] ブラウザを閉じます")
            logger.info("ブラウザクローズ")
            self.driver.quit()
            print("[DEBUG] ✅ ブラウザを閉じました")
            logger.info("ブラウザクローズ完了")


# ============================================
# メイン実行部分
# ============================================

def main():
    """メイン関数"""
    print("=" * 70)
    print("🔍 Selenium スクレイピングサポートツール")
    print("=" * 70)
    logger.info("プログラム開始")
    
    # スクレイピングサポートインスタンスを作成
    scraper = ScrapingSupport(headless=False)  # False=ブラウザ表示、True=非表示
    
    try:
        # ドライバーを起動
        if not scraper.start_driver():
            print("[DEBUG] ❌ ドライバー起動に失敗しました")
            return
        
        # スクレイピング対象のURL（ここを変更してください）
        # 例: 'https://example.com'
        url = input("\n分析するURLを入力してください: ")
        
        # URLを開く
        if not scraper.open_url(url):
            print("[DEBUG] ❌ URLを開けませんでした")
            return
        
        # ページ基本情報を取得
        page_info = scraper.get_page_info()
        
        # DOM構造を分析
        dom_analysis = scraper.analyze_dom_structure()
        
        # リンク一覧を取得
        links = scraper.find_all_links()
        
        # 画像一覧を取得
        images = scraper.find_all_images()
        
        # HTMLを保存
        html = scraper.get_full_html(save_to_file=True)
        
        # スクリーンショット保存
        scraper.save_screenshot()
        
        # サンプルコード生成
        sample_code = scraper.generate_scraping_code('class')
        
        print("\n" + "=" * 70)
        print("✅ 分析完了！")
        print("=" * 70)
        print(f"📄 ログファイル: scraping.log")
        print(f"💾 HTMLファイル: scraped_html_*.html")
        print(f"📸 スクリーンショット: screenshot_*.png")
        
        logger.info("分析完了")
        
    except Exception as e:
        print(f"\n[DEBUG] ❌ エラー発生: {e}")
        logger.error(f"予期しないエラー: {e}", exc_info=True)
    
    finally:
        # ブラウザを閉じる
        scraper.close()
        logger.info("プログラム終了")


# プログラムのエントリーポイント
if __name__ == "__main__":
    main()