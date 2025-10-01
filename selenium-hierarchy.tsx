import React, { useState } from 'react';
import { ChevronRight, Code, Lightbulb } from 'lucide-react';

const SeleniumAdvanced = () => {
  const [activeTab, setActiveTab] = useState('complex');

  const examples = {
    complex: [
      {
        title: 'テーブル内の特定セルを取得',
        html: '<table id="data-table">\n  <tr>\n    <td>名前</td>\n    <td>年齢</td>\n  </tr>\n  <tr>\n    <td>田中</td>\n    <td>25</td>\n  </tr>\n  <tr>\n    <td>佐藤</td>\n    <td>30</td>\n  </tr>\n</table>',
        xpath: '//table[@id="data-table"]//tr[3]/td[2]',
        css: '#data-table tr:nth-child(3) td:nth-child(2)',
        python: `# 佐藤の年齢を取得\nage = driver.find_element(\n  By.XPATH,\n  '//table[@id="data-table"]//tr[3]/td[2]'\n).text`,
        desc: '3行目の2列目（佐藤の年齢）を取得'
      },
      {
        title: '特定テキストを含む要素の兄弟要素',
        html: '<div class="user-card">\n  <span class="label">名前:</span>\n  <span class="value">山田太郎</span>\n</div>',
        xpath: '//span[text()="名前:"]/following-sibling::span',
        css: 'なし（CSSでは困難）',
        python: `# 「名前:」の次の要素を取得\nname = driver.find_element(\n  By.XPATH,\n  '//span[text()="名前:"]/following-sibling::span'\n).text`,
        desc: '特定テキストの次にある兄弟要素を取得'
      },
      {
        title: '複数条件での絞り込み',
        html: '<div class="product">\n  <h3>商品A</h3>\n  <span class="price">1000円</span>\n  <button class="btn">購入</button>\n</div>\n<div class="product sold-out">\n  <h3>商品B</h3>\n  <span class="price">2000円</span>\n  <button class="btn">購入</button>\n</div>',
        xpath: '//div[@class="product" and not(contains(@class, "sold-out"))]//button',
        css: 'div.product:not(.sold-out) button',
        python: `# 在庫ありの商品の購入ボタン\nbuttons = driver.find_elements(\n  By.CSS_SELECTOR,\n  'div.product:not(.sold-out) button'\n)`,
        desc: '売り切れでない商品のボタンのみ取得'
      },
      {
        title: '動的リストの最後の要素',
        html: '<ul id="notifications">\n  <li>通知1</li>\n  <li>通知2</li>\n  <li>通知3</li>\n  <!-- 動的に増える -->\n</ul>',
        xpath: '//ul[@id="notifications"]/li[last()]',
        css: '#notifications li:last-child',
        python: `# 最新の通知を取得\nlast_notification = driver.find_element(\n  By.CSS_SELECTOR,\n  '#notifications li:last-child'\n).text`,
        desc: '動的に追加される最後の要素を取得'
      }
    ],
    attribute: [
      {
        title: '部分一致で属性検索',
        html: '<input type="text"\n  placeholder="メールアドレスを入力"\n  name="user-email-input"/>',
        xpath: '//input[contains(@name, "email")]',
        css: 'input[name*="email"]',
        python: `# nameに"email"を含む入力欄\nemail_field = driver.find_element(\n  By.CSS_SELECTOR,\n  'input[name*="email"]'\n)`,
        desc: '属性値に特定文字列を含む要素を検索'
      },
      {
        title: '前方一致・後方一致',
        html: '<a href="https://example.com/page1">リンク1</a>\n<a href="https://example.com/page2">リンク2</a>\n<a href="download.pdf">PDF</a>',
        xpath: '//a[starts-with(@href, "https")]',
        css: 'a[href^="https"]',
        python: `# httpsで始まるリンクのみ\nlinks = driver.find_elements(\n  By.CSS_SELECTOR,\n  'a[href^="https"]'\n)\n\n# .pdfで終わるリンク\npdf_links = driver.find_elements(\n  By.CSS_SELECTOR,\n  'a[href$=".pdf"]'\n)`,
        desc: '^は前方一致、$は後方一致'
      },
      {
        title: '複数属性の組み合わせ',
        html: '<button type="submit"\n  class="btn primary"\n  data-action="save">保存</button>',
        xpath: '//button[@type="submit" and @data-action="save"]',
        css: 'button[type="submit"][data-action="save"]',
        python: `# 複数の属性で絞り込み\nsave_btn = driver.find_element(\n  By.CSS_SELECTOR,\n  'button[type="submit"][data-action="save"]'\n)`,
        desc: '複数の属性条件で要素を特定'
      },
      {
        title: '属性の有無で判定',
        html: '<input type="checkbox" checked>\n<input type="checkbox">\n<input type="checkbox" checked>',
        xpath: '//input[@checked]',
        css: 'input[checked]',
        python: `# チェック済みのチェックボックス\nchecked_boxes = driver.find_elements(\n  By.CSS_SELECTOR,\n  'input[checked]'\n)`,
        desc: '特定の属性を持つ要素のみ取得'
      }
    ],
    practical: [
      {
        title: 'フォーム全体の操作',
        html: '<form id="login-form">\n  <input name="username"/>\n  <input name="password" type="password"/>\n  <button type="submit">ログイン</button>\n</form>',
        python: `# フォーム要素をまとめて取得
form = driver.find_element(By.ID, "login-form")
username = form.find_element(By.NAME, "username")
password = form.find_element(By.NAME, "password")
submit = form.find_element(By.CSS_SELECTOR, "button[type='submit']")

# 入力と送信
username.send_keys("user@example.com")
password.send_keys("password123")
submit.click()`,
        desc: 'フォーム要素を親から取得して操作'
      },
      {
        title: '動的に読み込まれる要素の待機',
        python: `from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 要素が表示されるまで最大10秒待機
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, "//div[@class='loaded-content']//button")
    )
)

# 要素がクリック可能になるまで待機
button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button.dynamic-btn")
    )
)`,
        desc: '階層指定と待機処理を組み合わせる'
      },
      {
        title: 'ドロップダウンメニューの選択',
        html: '<div class="dropdown">\n  <button class="dropdown-toggle">選択</button>\n  <ul class="dropdown-menu">\n    <li data-value="1">オプション1</li>\n    <li data-value="2">オプション2</li>\n  </ul>\n</div>',
        python: `# ドロップダウンを開く
dropdown = driver.find_element(By.CLASS_NAME, "dropdown")
dropdown.find_element(By.CLASS_NAME, "dropdown-toggle").click()

# 特定のオプションを選択
option = dropdown.find_element(
    By.XPATH,
    ".//li[@data-value='2']"
)
option.click()`,
        desc: '親要素から相対パスで子要素を操作'
      },
      {
        title: 'ページネーション処理',
        python: `# 全ページのデータを収集
all_data = []

while True:
    # 現在ページのアイテムを取得
    items = driver.find_elements(
        By.CSS_SELECTOR,
        "div.item-list > div.item"
    )
    
    for item in items:
        title = item.find_element(By.CLASS_NAME, "title").text
        all_data.append(title)
    
    # 次ページボタンを探す
    try:
        next_btn = driver.find_element(
            By.XPATH,
            "//button[contains(text(), '次へ') and not(@disabled)]"
        )
        next_btn.click()
        time.sleep(2)  # ページ読み込み待機
    except:
        break  # 次ページがない場合は終了`,
        desc: '階層指定を使った複数ページの自動巡回'
      }
    ]
  };

  return (
    <div className="w-full max-w-5xl mx-auto p-6 bg-gradient-to-br from-blue-50 to-indigo-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Selenium 階層指定 - 応用編
        </h1>
        <p className="text-gray-600 text-lg">
          実践的な要素指定テクニックと複雑なケースへの対応
        </p>
      </div>

      {/* タブ */}
      <div className="flex gap-2 mb-6 border-b-2 bg-white rounded-t-lg">
        <button
          onClick={() => setActiveTab('complex')}
          className={`px-6 py-3 font-medium transition-all ${
            activeTab === 'complex'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
          }`}
        >
          複雑な階層指定
        </button>
        <button
          onClick={() => setActiveTab('attribute')}
          className={`px-6 py-3 font-medium transition-all ${
            activeTab === 'attribute'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
          }`}
        >
          属性による検索
        </button>
        <button
          onClick={() => setActiveTab('practical')}
          className={`px-6 py-3 font-medium transition-all ${
            activeTab === 'practical'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
              : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
          }`}
        >
          実践コード例
        </button>
      </div>

      {/* コンテンツ */}
      <div className="space-y-6">
        {examples[activeTab].map((example, index) => (
          <div
            key={index}
            className="border-2 border-gray-200 rounded-xl p-6 bg-white hover:shadow-xl transition-all duration-300"
          >
            <div className="flex items-start gap-3 mb-4">
              <div className="bg-gradient-to-br from-blue-500 to-indigo-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold text-lg shadow-md">
                {index + 1}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mt-1">
                {example.title}
              </h3>
            </div>

            {example.html && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <Code size={18} className="text-indigo-600" />
                  HTML構造
                </div>
                <pre className="bg-gray-900 p-4 rounded-lg border-2 border-gray-700 text-sm overflow-x-auto">
                  <code className="text-green-300">{example.html}</code>
                </pre>
              </div>
            )}

            {example.xpath && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <ChevronRight size={18} className="text-orange-600" />
                  XPath
                </div>
                <pre className="bg-orange-900 text-orange-100 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                  <code>{example.xpath}</code>
                </pre>
              </div>
            )}

            {example.css && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <ChevronRight size={18} className="text-purple-600" />
                  CSS Selector
                </div>
                <pre className="bg-purple-900 text-purple-100 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                  <code>{example.css}</code>
                </pre>
              </div>
            )}

            {example.python && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <Code size={18} className="text-blue-600" />
                  Python コード
                </div>
                <pre className="bg-blue-950 text-blue-100 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                  <code>{example.python}</code>
                </pre>
              </div>
            )}

            <div className="flex items-start gap-3 bg-gradient-to-r from-amber-50 to-yellow-50 p-4 rounded-lg border-l-4 border-amber-400">
              <Lightbulb className="text-amber-600 mt-0.5 flex-shrink-0" size={20} />
              <p className="text-gray-700 font-medium">{example.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* 補足情報 */}
      <div className="mt-8 p-6 bg-white border-l-4 border-indigo-500 rounded-lg shadow-md">
        <h4 className="font-bold text-gray-800 mb-4 text-xl flex items-center gap-2">
          <Lightbulb className="text-indigo-600" />
          応用テクニックのポイント
        </h4>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div className="bg-indigo-50 p-3 rounded">
            <strong className="text-indigo-700">階層の組み合わせ</strong>
            <p className="mt-1">親要素から段階的に絞り込むことで、より正確な要素特定が可能</p>
          </div>
          <div className="bg-purple-50 p-3 rounded">
            <strong className="text-purple-700">属性の活用</strong>
            <p className="mt-1">contains()や部分一致を使って柔軟な検索を実現</p>
          </div>
          <div className="bg-blue-50 p-3 rounded">
            <strong className="text-blue-700">待機処理</strong>
            <p className="mt-1">動的コンテンツでは WebDriverWait との組み合わせが重要</p>
          </div>
          <div className="bg-green-50 p-3 rounded">
            <strong className="text-green-700">相対パス</strong>
            <p className="mt-1">親要素から相対的に検索することでコードの保守性が向上</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeleniumAdvanced;