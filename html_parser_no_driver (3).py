# ============================================
# ドライバー不要 HTML解析ツール
# BeautifulSoup + requests でスクレイピング
# Seleniumドライバー不要で超高速！
# ============================================

# --- 必要なモジュールをインポート ---
import requests  # HTTP通信でWebページを取得するライブラリ
from bs4 import BeautifulSoup  # HTMLを解析するライブラリ（BeautifulSoup4）
import logging  # ログ出力用の標準ライブラリ
from datetime import datetime  # 現在日時の取得用
from typing import List, Dict, Optional # ============================================
# ドライバー不要 HTML解析ツール
# BeautifulSoup + requests でスクレイピング
# ============================================

import requests  # HTTP通信用
from bs4 import BeautifulSoup  # HTML解析用
import logging  # ログ出力用
from datetime import datetime  # 日時取得用
from typing import List, Dict, Optional  # 型ヒント用
from urllib.parse import urljoin, urlparse  # URL処理用
import json  # JSON出力用
import csv  # CSV出力用


# ============================================
# ログ設定
# ============================================

logging.basicConfig(
    level=logging.DEBUG,  # DEBUGレベル以上を出力
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('html_analysis.log', encoding='utf-8'),  # ファイルに保存
        logging.StreamHandler()  # コンソールにも表示
    ]
)

logger = logging.getLogger(__name__)


# ============================================
# HTML解析クラス
# ============================================

class HTMLAnalyzer:
    """
    ドライバー不要でHTMLを解析するクラス
    requests + BeautifulSoup を使用
    """
    
    def __init__(self):
        """初期化"""
        print("[DEBUG] HTMLAnalyzerを初期化")
        logger.info("HTMLAnalyzer初期化")
        
        # リクエスト用のヘッダー設定（ボット検出を回避）
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        self.soup = None  # BeautifulSoupオブジェクトを保存
        self.url = None  # 現在のURL
        self.html = None  # HTML文字列
    
    def fetch_url(self, url: str, timeout: int = 10) -> bool:
        """
        URLからHTMLを取得
        
        Args:
            url: 取得するURL
            timeout: タイムアウト時間（秒）
            
        Returns:
            成功時True、失敗時False
        """
        print(f"\n[DEBUG] URLにアクセス: {url}")
        logger.info(f"URL取得開始: {url}")
        
        try:
            # HTTPリクエストを送信
            response = requests.get(url, headers=self.headers, timeout=timeout)
            
            # ステータスコードを確認
            print(f"[DEBUG] ステータスコード: {response.status_code}")
            logger.debug(f"ステータスコード: {response.status_code}")
            
            # エラーチェック
            response.raise_for_status()  # 4xx, 5xxエラーの場合は例外を発生
            
            # エンコーディングを設定（文字化け対策）
            if response.encoding == 'ISO-8859-1':  # デフォルトエンコーディングの場合
                response.encoding = response.apparent_encoding  # 自動検出
            
            # HTMLを保存
            self.html = response.text
            self.url = url
            
            # BeautifulSoupでパース
            self.soup = BeautifulSoup(self.html, 'html.parser')
            
            print(f"[DEBUG] ✅ HTML取得成功")
            print(f"[DEBUG] HTML長: {len(self.html):,} 文字")
            print(f"[DEBUG] エンコーディング: {response.encoding}")
            
            logger.info(f"HTML取得成功: {len(self.html)}文字")
            logger.debug(f"エンコーディング: {response.encoding}")
            
            return True
            
        except requests.exceptions.Timeout:
            print(f"[DEBUG] ❌ タイムアウト: {timeout}秒以内に応答がありませんでした")
            logger.error(f"タイムアウト: {url}")
            return False
            
        except requests.exceptions.HTTPError as e:
            print(f"[DEBUG] ❌ HTTPエラー: {e}")
            logger.error(f"HTTPエラー: {e}")
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"[DEBUG] ❌ リクエストエラー: {e}")
            logger.error(f"リクエストエラー: {e}", exc_info=True)
            return False
    
    def load_from_file(self, filepath: str) -> bool:
        """
        ローカルのHTMLファイルを読み込む
        
        Args:
            filepath: HTMLファイルのパス
            
        Returns:
            成功時True、失敗時False
        """
        print(f"\n[DEBUG] ファイルを読み込み: {filepath}")
        logger.info(f"ファイル読み込み: {filepath}")
        
        try:
            # ファイルを読み込む
            with open(filepath, 'r', encoding='utf-8') as f:
                self.html = f.read()
            
            # BeautifulSoupでパース
            self.soup = BeautifulSoup(self.html, 'html.parser')
            self.url = f"file://{filepath}"
            
            print(f"[DEBUG] ✅ ファイル読み込み成功")
            print(f"[DEBUG] HTML長: {len(self.html):,} 文字")
            
            logger.info(f"ファイル読み込み成功: {len(self.html)}文字")
            
            return True
            
        except FileNotFoundError:
            print(f"[DEBUG] ❌ ファイルが見つかりません: {filepath}")
            logger.error(f"ファイル未発見: {filepath}")
            return False
            
        except Exception as e:
            print(f"[DEBUG] ❌ ファイル読み込みエラー: {e}")
            logger.error(f"ファイル読み込みエラー: {e}", exc_info=True)
            return False
    
    def get_page_info(self) -> Dict[str, any]:
        """
        ページの基本情報を取得
        
        Returns:
            ページ情報の辞書
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            logger.warning("HTML未読み込み")
            return {}
        
        print("\n[DEBUG] ========== ページ基本情報 ==========")
        logger.info("ページ情報取得開始")
        
        # タイトルを取得
        title = self.soup.title.string if self.soup.title else "(タイトルなし)"
        
        # メタ情報を取得
        description = ""
        keywords = ""
        
        # descriptionメタタグ
        meta_desc = self.soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            description = meta_desc.get('content', '')
        
        # keywordsメタタグ
        meta_keywords = self.soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            keywords = meta_keywords.get('content', '')
        
        info = {
            'url': self.url,
            'title': title,
            'description': description,
            'keywords': keywords,
            'html_length': len(self.html)
        }
        
        # 情報を表示
        print(f"[DEBUG] URL: {info['url']}")
        print(f"[DEBUG] タイトル: {info['title']}")
        print(f"[DEBUG] 説明: {info['description'][:100] if info['description'] else '(なし)'}...")
        print(f"[DEBUG] キーワード: {info['keywords'][:100] if info['keywords'] else '(なし)'}...")
        print(f"[DEBUG] HTML長: {info['html_length']:,} 文字")
        
        logger.info(f"ページ情報: {title}")
        logger.debug(f"HTML長: {info['html_length']}")
        
        return info
    
    def analyze_structure(self) -> Dict[str, int]:
        """
        HTML構造を分析（要素数をカウント）
        
        Returns:
            要素数の辞書
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return {}
        
        print("\n[DEBUG] ========== HTML構造分析 ==========")
        logger.info("構造分析開始")
        
        # 主要な要素をカウント
        elements = [
            'div', 'span', 'p', 'a', 'img', 'table', 'tr', 'td',
            'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'form', 'input', 'button', 'select', 'textarea',
            'nav', 'header', 'footer', 'section', 'article', 'aside'
        ]
        
        counts = {}
        
        print("[DEBUG] 要素数をカウント中...")
        
        for element in elements:
            # 要素を検索してカウント
            found = self.soup.find_all(element)
            count = len(found)
            counts[element] = count
            
            if count > 0:  # 存在する要素のみ表示
                print(f"[DEBUG]   <{element}>: {count}個")
                logger.debug(f"要素: <{element}> = {count}")
        
        logger.info(f"構造分析完了: {len(counts)}種類の要素")
        
        return counts
    
    def find_by_class(self, class_name: str) -> List:
        """
        クラス名で要素を検索
        
        Args:
            class_name: 検索するクラス名
            
        Returns:
            見つかった要素のリスト
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return []
        
        print(f"\n[DEBUG] クラス名で検索: '{class_name}'")
        logger.info(f"クラス検索: {class_name}")
        
        # クラス名で検索
        elements = self.soup.find_all(class_=class_name)
        
        print(f"[DEBUG] ✅ {len(elements)}個の要素が見つかりました")
        logger.info(f"クラス検索結果: {len(elements)}個")
        
        # 各要素の情報を表示
        for i, element in enumerate(elements[:5], 1):  # 最初の5個
            text = element.get_text(strip=True)[:50]
            tag = element.name
            print(f"[DEBUG]   [{i}] <{tag}> {text}...")
            logger.debug(f"要素[{i}]: <{tag}> {text[:30]}")
        
        if len(elements) > 5:
            print(f"[DEBUG]   ... 他 {len(elements) - 5}個")
        
        return elements
    
    def find_by_id(self, element_id: str):
        """
        IDで要素を検索
        
        Args:
            element_id: 検索する要素のID
            
        Returns:
            見つかった要素またはNone
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return None
        
        print(f"\n[DEBUG] IDで検索: '{element_id}'")
        logger.info(f"ID検索: {element_id}")
        
        # IDで検索
        element = self.soup.find(id=element_id)
        
        if element:
            text = element.get_text(strip=True)[:100]
            tag = element.name
            print(f"[DEBUG] ✅ 要素が見つかりました")
            print(f"[DEBUG]   タグ: <{tag}>")
            print(f"[DEBUG]   テキスト: {text}...")
            logger.info(f"ID検索成功: {element_id}")
        else:
            print(f"[DEBUG] ❌ 要素が見つかりません")
            logger.warning(f"ID検索失敗: {element_id}")
        
        return element
    
    def find_by_tag(self, tag_name: str) -> List:
        """
        タグ名で要素を検索
        
        Args:
            tag_name: 検索するタグ名
            
        Returns:
            見つかった要素のリスト
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return []
        
        print(f"\n[DEBUG] タグ名で検索: '<{tag_name}>'")
        logger.info(f"タグ検索: {tag_name}")
        
        # タグ名で検索
        elements = self.soup.find_all(tag_name)
        
        print(f"[DEBUG] ✅ {len(elements)}個の要素が見つかりました")
        logger.info(f"タグ検索結果: {len(elements)}個")
        
        return elements
    
    def find_by_css_selector(self, selector: str) -> List:
        """
        CSSセレクタで要素を検索
        
        Args:
            selector: CSSセレクタ
            
        Returns:
            見つかった要素のリスト
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return []
        
        print(f"\n[DEBUG] CSSセレクタで検索: '{selector}'")
        logger.info(f"CSS検索: {selector}")
        
        # CSSセレクタで検索
        elements = self.soup.select(selector)
        
        print(f"[DEBUG] ✅ {len(elements)}個の要素が見つかりました")
        logger.info(f"CSS検索結果: {len(elements)}個")
        
        # 各要素の情報を表示
        for i, element in enumerate(elements[:5], 1):
            text = element.get_text(strip=True)[:50]
            tag = element.name
            print(f"[DEBUG]   [{i}] <{tag}> {text}...")
            logger.debug(f"要素[{i}]: <{tag}> {text[:30]}")
        
        if len(elements) > 5:
            print(f"[DEBUG]   ... 他 {len(elements) - 5}個")
        
        return elements
    
    def get_all_links(self) -> List[Dict[str, str]]:
        """
        すべてのリンクを取得
        
        Returns:
            リンク情報のリスト
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return []
        
        print("\n[DEBUG] ========== リンク一覧 ==========")
        logger.info("リンク取得開始")
        
        # すべての<a>タグを検索
        links = self.soup.find_all('a')
        
        link_data = []
        
        print(f"[DEBUG] {len(links)}個のリンクが見つかりました")
        logger.info(f"リンク数: {len(links)}")
        
        # 各リンクの情報を取得
        for i, link in enumerate(links[:10], 1):  # 最初の10個
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            if href:
                # 相対URLを絶対URLに変換
                absolute_url = urljoin(self.url, href) if self.url else href
                
                link_info = {
                    'href': absolute_url,
                    'text': text if text else '(テキストなし)',
                    'original_href': href
                }
                link_data.append(link_info)
                
                print(f"[DEBUG]   [{i}] {link_info['text'][:40]}")
                print(f"[DEBUG]       → {absolute_url}")
                logger.debug(f"リンク[{i}]: {text[:30]} -> {href}")
        
        if len(links) > 10:
            print(f"[DEBUG]   ... 他 {len(links) - 10}個")
        
        logger.info(f"リンク取得完了: {len(link_data)}個")
        
        return link_data
    
    def get_all_images(self) -> List[Dict[str, str]]:
        """
        すべての画像を取得
        
        Returns:
            画像情報のリスト
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return []
        
        print("\n[DEBUG] ========== 画像一覧 ==========")
        logger.info("画像取得開始")
        
        # すべての<img>タグを検索
        images = self.soup.find_all('img')
        
        image_data = []
        
        print(f"[DEBUG] {len(images)}個の画像が見つかりました")
        logger.info(f"画像数: {len(images)}")
        
        # 各画像の情報を取得
        for i, img in enumerate(images[:10], 1):  # 最初の10個
            src = img.get('src', '')
            alt = img.get('alt', '')
            
            if src:
                # 相対URLを絶対URLに変換
                absolute_url = urljoin(self.url, src) if self.url else src
                
                img_info = {
                    'src': absolute_url,
                    'alt': alt if alt else '(altなし)',
                    'original_src': src
                }
                image_data.append(img_info)
                
                print(f"[DEBUG]   [{i}] alt='{img_info['alt'][:40]}'")
                print(f"[DEBUG]       src: {absolute_url[:60]}...")
                logger.debug(f"画像[{i}]: alt={alt} -> {src[:50]}")
        
        if len(images) > 10:
            print(f"[DEBUG]   ... 他 {len(images) - 10}個")
        
        logger.info(f"画像取得完了: {len(image_data)}個")
        
        return image_data
    
    def save_html(self, filename: Optional[str] = None):
        """
        HTMLをファイルに保存
        
        Args:
            filename: 保存するファイル名
        """
        if not self.html:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return
        
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'saved_html_{timestamp}.html'
        
        print(f"\n[DEBUG] HTMLをファイルに保存: {filename}")
        logger.info(f"HTML保存: {filename}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.html)
            
            print(f"[DEBUG] ✅ 保存成功: {len(self.html):,} 文字")
            logger.info(f"HTML保存完了: {len(self.html)}文字")
            
        except Exception as e:
            print(f"[DEBUG] ❌ 保存エラー: {e}")
            logger.error(f"HTML保存エラー: {e}")
    
    def extract_text(self) -> str:
        """
        HTMLからテキストのみを抽出
        
        Returns:
            テキスト文字列
        """
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return ""
        
        print("\n[DEBUG] テキストを抽出中...")
        logger.info("テキスト抽出開始")
        
        # テキストのみを取得
        text = self.soup.get_text(separator='\n', strip=True)
        
        print(f"[DEBUG] ✅ テキスト抽出完了: {len(text):,} 文字")
        logger.info(f"テキスト抽出完了: {len(text)}文字")
        
        return text
    
    def pretty_print(self):
        """HTMLを整形して表示"""
        if not self.soup:
            print("[DEBUG] ❌ HTMLが読み込まれていません")
            return
        
        print("\n[DEBUG] ========== 整形HTML ==========")
        
        # prettify()で整形
        pretty_html = self.soup.prettify()
        
        # 最初の50行のみ表示
        lines = pretty_html.split('\n')[:50]
        print('\n'.join(lines))
        
        if len(pretty_html.split('\n')) > 50:
            print(f"\n... 他 {len(pretty_html.split('\n')) - 50}行")


# ============================================
# メイン実行部分
# ============================================

def main():
    """メイン関数"""
    print("=" * 70)
    print("🔍 ドライバー不要 HTML解析ツール")
    print("=" * 70)
    logger.info("プログラム開始")
    
    analyzer = HTMLAnalyzer()
    
    print("\n解析方法を選択:")
    print("1. URLから取得")
    print("2. ローカルファイルから読み込み")
    
    choice = input("\n選択 (1-2): ")
    
    try:
        if choice == "1":
            # URLから取得
            url = input("URL: ")
            if not analyzer.fetch_url(url):
                print("[DEBUG] ❌ HTML取得に失敗しました")
                return
        
        elif choice == "2":
            # ファイルから読み込み
            filepath = input("HTMLファイルのパス: ")
            if not analyzer.load_from_file(filepath):
                print("[DEBUG] ❌ ファイル読み込みに失敗しました")
                return
        
        else:
            print("[DEBUG] ❌ 無効な選択です")
            return
        
        # ページ情報を取得
        page_info = analyzer.get_page_info()
        
        # 構造を分析
        structure = analyzer.analyze_structure()
        
        # リンク一覧
        links = analyzer.get_all_links()
        
        # 画像一覧
        images = analyzer.get_all_images()
        
        # HTMLを保存
        analyzer.save_html()
        
        # インタラクティブモード
        print("\n" + "=" * 70)
        print("📋 インタラクティブモード")
        print("=" * 70)
        print("コマンド:")
        print("  class <クラス名>  - クラスで検索")
        print("  id <ID>          - IDで検索")
        print("  tag <タグ名>      - タグで検索")
        print("  css <セレクタ>    - CSSセレクタで検索")
        print("  text             - テキストを抽出")
        print("  quit             - 終了")
        
        while True:
            command = input("\n> ").strip()
            
            if command == "quit":
                break
            
            elif command.startswith("class "):
                class_name = command[6:].strip()
                analyzer.find_by_class(class_name)
            
            elif command.startswith("id "):
                element_id = command[3:].strip()
                analyzer.find_by_id(element_id)
            
            elif command.startswith("tag "):
                tag_name = command[4:].strip()
                results = analyzer.find_by_tag(tag_name)
                print(f"[DEBUG] {len(results)}個見つかりました")
            
            elif command.startswith("css "):
                selector = command[4:].strip()
                analyzer.find_by_css_selector(selector)
            
            elif command == "text":
                text = analyzer.extract_text()
                print(f"\n{text[:500]}...")  # 最初の500文字
            
            else:
                print("[DEBUG] 不明なコマンド")
        
        print("\n" + "=" * 70)
        print("✅ 解析完了")
        print("=" * 70)
        logger.info("プログラム終了")
    
    except KeyboardInterrupt:
        print("\n\n[DEBUG] 中断されました")
        logger.info("ユーザー中断")
    
    except Exception as e:
        print(f"\n[DEBUG] ❌ エラー: {e}")
        logger.error(f"エラー: {e}", exc_info=True)


if __name__ == "__main__":
    main()