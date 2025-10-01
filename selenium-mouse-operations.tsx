import React, { useState } from 'react';
import { Mouse, Hand, Move, Target, Lightbulb, ZoomIn } from 'lucide-react';

const SeleniumMouseOps = () => {
  const [activeTab, setActiveTab] = useState('click');

  const examples = {
    click: [
      {
        title: '基本的なクリック',
        visual: 'single-click',
        python: `# 通常のクリック
element = driver.find_element(By.ID, "button")
element.click()

# ActionChainsを使ったクリック
from selenium.webdriver.common.action_chains import ActionChains
actions = ActionChains(driver)
actions.click(element).perform()`,
        desc: '最も基本的なマウスクリック操作'
      },
      {
        title: 'ダブルクリック',
        visual: 'double-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.CLASS_NAME, "editable-text")
actions = ActionChains(driver)

# ダブルクリック
actions.double_click(element).perform()

# テキストが選択される
print(element.text)`,
        desc: 'テキスト選択やファイル開封に使用'
      },
      {
        title: '右クリック（コンテキストメニュー）',
        visual: 'right-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.ID, "context-area")
actions = ActionChains(driver)

# 右クリック
actions.context_click(element).perform()

# コンテキストメニューが表示される
time.sleep(1)

# メニュー項目を選択
menu_item = driver.find_element(By.XPATH, "//div[@class='menu-item']")
menu_item.click()`,
        desc: 'コンテキストメニューを開く'
      },
      {
        title: 'Ctrlキー + クリック（複数選択）',
        visual: 'ctrl-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

actions = ActionChains(driver)

# 複数の項目をCtrl+クリックで選択
items = driver.find_elements(By.CLASS_NAME, "selectable-item")

actions.key_down(Keys.CONTROL)

for item in items[::2]:  # 偶数番目を選択
    actions.click(item)

actions.key_up(Keys.CONTROL)
actions.perform()`,
        desc: '複数要素の同時選択'
      }
    ],
    hover: [
      {
        title: 'マウスホバー',
        visual: 'hover',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.CLASS_NAME, "menu-trigger")
actions = ActionChains(driver)

# 要素にマウスを乗せる
actions.move_to_element(element).perform()

# ホバーメニューが表示されるまで待機
time.sleep(1)

# ドロップダウンメニューの項目をクリック
submenu = driver.find_element(By.CLASS_NAME, "dropdown-item")
submenu.click()`,
        desc: 'ドロップダウンメニューやツールチップの表示'
      },
      {
        title: 'ホバー後に要素をクリック',
        visual: 'hover-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# メニューにホバー
menu = driver.find_element(By.ID, "main-menu")
submenu_item = driver.find_element(By.ID, "submenu-option")

actions = ActionChains(driver)
actions.move_to_element(menu)\\
    .pause(0.5)\\
    .move_to_element(submenu_item)\\
    .click()\\
    .perform()`,
        desc: 'ホバーとクリックを連続で実行'
      },
      {
        title: '複数段階のホバー',
        visual: 'nested-hover',
        python: `from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# 多段階メニューをナビゲート
level1 = driver.find_element(By.ID, "menu-level1")
level2 = driver.find_element(By.ID, "menu-level2")
level3 = driver.find_element(By.ID, "menu-level3")

actions.move_to_element(level1)\\
    .pause(0.3)\\
    .move_to_element(level2)\\
    .pause(0.3)\\
    .move_to_element(level3)\\
    .click()\\
    .perform()`,
        desc: '入れ子のメニューを順番にホバー'
      },
      {
        title: 'ホバーによる画像プレビュー',
        visual: 'image-preview',
        python: `from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

thumbnail = driver.find_element(By.CLASS_NAME, "thumbnail")
actions = ActionChains(driver)

# サムネイルにホバー
actions.move_to_element(thumbnail).perform()

# プレビューが表示されるまで待機
preview = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located(
        (By.CLASS_NAME, "preview-popup")
    )
)

# プレビュー画像のURLを取得
preview_url = preview.find_element(
    By.TAG_NAME, "img"
).get_attribute("src")`,
        desc: 'ホバーで表示される画像プレビューを取得'
      }
    ],
    drag: [
      {
        title: '基本的なドラッグ&ドロップ',
        visual: 'drag-basic',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# ドラッグ元とドロップ先を取得
source = driver.find_element(By.ID, "draggable")
target = driver.find_element(By.ID, "droppable")

actions = ActionChains(driver)

# ドラッグ&ドロップを実行
actions.drag_and_drop(source, target).perform()

# または手動で制御
actions.click_and_hold(source)\\
    .move_to_element(target)\\
    .release()\\
    .perform()`,
        desc: '要素間のドラッグ&ドロップ'
      },
      {
        title: 'オフセットでドラッグ',
        visual: 'drag-offset',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.CLASS_NAME, "movable")
actions = ActionChains(driver)

# 要素を相対座標でドラッグ
actions.click_and_hold(element)\\
    .move_by_offset(100, 50)\\
    .release()\\
    .perform()

# または drag_and_drop_by_offset を使用
actions.drag_and_drop_by_offset(
    element, 
    100,  # X方向
    50    # Y方向
).perform()`,
        desc: '座標指定で要素をドラッグ'
      },
      {
        title: 'スライダーのドラッグ',
        visual: 'slider-drag',
        python: `from selenium.webdriver.common.action_chains import ActionChains

slider = driver.find_element(By.CLASS_NAME, "slider-handle")
actions = ActionChains(driver)

# スライダーを50%の位置に移動
slider_track = driver.find_element(By.CLASS_NAME, "slider-track")
track_width = slider_track.size['width']

# スライダーを中央に移動
actions.click_and_hold(slider)\\
    .move_by_offset(track_width // 2, 0)\\
    .release()\\
    .perform()

# 値を取得
value = slider.get_attribute("aria-valuenow")
print(f"Slider value: {value}")`,
        desc: 'レンジスライダーをドラッグ操作'
      },
      {
        title: 'リストアイテムの並び替え',
        visual: 'sortable-list',
        python: `from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# 3番目の項目を1番目に移動
items = driver.find_elements(By.CLASS_NAME, "sortable-item")
item_to_move = items[2]
target_position = items[0]

# ドラッグで並び替え
actions.click_and_hold(item_to_move)\\
    .move_to_element(target_position)\\
    .release()\\
    .perform()

time.sleep(1)

# 新しい順序を確認
new_items = driver.find_elements(By.CLASS_NAME, "sortable-item")
for i, item in enumerate(new_items):
    print(f"{i+1}: {item.text}")`,
        desc: 'ソート可能なリストの項目を並び替え'
      }
    ],
    advanced: [
      {
        title: 'マウスの軌跡を描く',
        visual: 'mouse-trail',
        python: `from selenium.webdriver.common.action_chains import ActionChains
import math

canvas = driver.find_element(By.ID, "drawing-canvas")
actions = ActionChains(driver)

# 円を描く
def draw_circle(center_x, center_y, radius, steps=36):
    actions.move_to_element_with_offset(
        canvas, 
        center_x + radius, 
        center_y
    ).click_and_hold()
    
    for i in range(steps + 1):
        angle = 2 * math.pi * i / steps
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        actions.move_to_element_with_offset(canvas, x, y)
    
    actions.release().perform()

draw_circle(0, 0, 50)`,
        desc: 'マウスで図形を描画'
      },
      {
        title: 'マウスホイールスクロール',
        visual: 'scroll',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.ID, "scrollable-area")
actions = ActionChains(driver)

# 要素上でスクロール（Selenium 4.0+）
actions.move_to_element(element)\\
    .scroll_by_amount(0, 500)\\
    .perform()

# または JavaScript で実行
driver.execute_script(
    "arguments[0].scrollTop = 500", 
    element
)

# ページ全体をスクロール
driver.execute_script("window.scrollBy(0, 500);")`,
        desc: 'マウスホイールによるスクロール'
      },
      {
        title: '長押し（ロングプレス）',
        visual: 'long-press',
        python: `from selenium.webdriver.common.action_chains import ActionChains
import time

element = driver.find_element(By.CLASS_NAME, "long-press-target")
actions = ActionChains(driver)

# 要素を2秒間長押し
actions.click_and_hold(element)\\
    .pause(2)\\
    .release()\\
    .perform()

# コンテキストメニューやツールチップが表示される
time.sleep(0.5)
tooltip = driver.find_element(By.CLASS_NAME, "tooltip")
print(f"Tooltip: {tooltip.text}")`,
        desc: '要素の長押し操作'
      },
      {
        title: 'マウスアウト検知',
        visual: 'mouse-out',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.ID, "hover-sensitive")
actions = ActionChains(driver)

# 要素にホバー
actions.move_to_element(element).perform()
time.sleep(1)

# 要素から離れる
actions.move_by_offset(100, 0).perform()

# または別の要素に移動
other_element = driver.find_element(By.ID, "other-area")
actions.move_to_element(other_element).perform()

# 元の要素が非表示になったか確認
is_visible = element.is_displayed()
print(f"Element still visible: {is_visible}")`,
        desc: 'マウスアウト時の動作を確認'
      }
    ],
    chain: [
      {
        title: '複数操作のチェーン',
        visual: 'action-chain',
        python: `from selenium.webdriver.common.action_chains import ActionChains

actions = ActionChains(driver)

# 複数の操作を連続実行
element1 = driver.find_element(By.ID, "step1")
element2 = driver.find_element(By.ID, "step2")
element3 = driver.find_element(By.ID, "step3")

actions.move_to_element(element1)\\
    .click()\\
    .pause(0.5)\\
    .move_to_element(element2)\\
    .double_click()\\
    .pause(0.5)\\
    .move_to_element(element3)\\
    .context_click()\\
    .perform()`,
        desc: '複数のマウス操作を一連のチェーンとして実行'
      },
      {
        title: 'ドラッグ中のホバー',
        visual: 'drag-hover',
        python: `from selenium.webdriver.common.action_chains import ActionChains

draggable = driver.find_element(By.ID, "draggable")
dropzone1 = driver.find_element(By.ID, "dropzone1")
dropzone2 = driver.find_element(By.ID, "dropzone2")

actions = ActionChains(driver)

# ドラッグ中に複数のドロップゾーンをホバー
actions.click_and_hold(draggable)\\
    .move_to_element(dropzone1)\\
    .pause(0.5)\\
    .move_to_element(dropzone2)\\
    .release()\\
    .perform()`,
        desc: 'ドラッグ中に複数の領域をホバー'
      },
      {
        title: 'マルチタッチシミュレーション',
        visual: 'multi-touch',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# ピンチズーム風の操作
element = driver.find_element(By.ID, "zoomable-image")

actions = ActionChains(driver)

# 中心から外側へ移動（ズームイン）
actions.move_to_element(element)\\
    .click_and_hold()\\
    .move_by_offset(100, 0)\\
    .release()\\
    .perform()

# JavaScript でズーム操作
driver.execute_script(
    "arguments[0].style.transform = 'scale(1.5)';",
    element
)`,
        desc: 'マルチタッチ操作のシミュレート'
      },
      {
        title: 'パフォーマンステスト',
        visual: 'performance',
        python: `from selenium.webdriver.common.action_chains import ActionChains
import time

# 連続クリックの速度テスト
button = driver.find_element(By.ID, "click-counter")
actions = ActionChains(driver)

start_time = time.time()
click_count = 0

# 5秒間に何回クリックできるか
while time.time() - start_time < 5:
    actions.click(button).perform()
    click_count += 1

print(f"Clicks in 5 seconds: {click_count}")

# 結果を確認
counter_value = button.text
print(f"Counter value: {counter_value}")`,
        desc: '高速連続クリックのテスト'
      }
    ]
  };

  const DemoBox = ({ type }) => {
    const commonStyles = "relative bg-gray-100 h-48 rounded-lg border-2 border-gray-300";
    
    switch(type) {
      case 'single-click':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <button className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-3 px-6 rounded-lg shadow-lg cursor-pointer transition-all">
              クリック
            </button>
          </div>
        );
      
      case 'double-click':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="bg-yellow-100 border-2 border-yellow-400 p-4 rounded">
              <span className="text-gray-700">ダブルクリックでテキスト選択</span>
            </div>
          </div>
        );
      
      case 'right-click':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="relative bg-green-500 text-white font-bold py-3 px-6 rounded-lg">
              右クリック
              <div className="absolute top-12 left-0 bg-white border shadow-lg rounded text-gray-700 text-sm font-normal w-32">
                <div className="px-3 py-2 hover:bg-gray-100">コピー</div>
                <div className="px-3 py-2 hover:bg-gray-100">貼り付け</div>
              </div>
            </div>
          </div>
        );
      
      case 'ctrl-click':
        return (
          <div className={`${commonStyles} flex items-center justify-center gap-4`}>
            {[1, 2, 3, 4].map(n => (
              <div key={n} className={`w-16 h-16 rounded flex items-center justify-center font-bold text-white ${n % 2 === 0 ? 'bg-purple-500' : 'bg-gray-400'}`}>
                {n}
              </div>
            ))}
          </div>
        );
      
      case 'hover':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="relative">
              <button className="bg-indigo-500 text-white font-bold py-3 px-6 rounded-lg">
                メニュー ▼
              </button>
              <div className="absolute top-12 left-0 bg-white border shadow-lg rounded w-40">
                <div className="px-4 py-2 hover:bg-gray-100">項目 1</div>
                <div className="px-4 py-2 hover:bg-gray-100">項目 2</div>
                <div className="px-4 py-2 hover:bg-gray-100">項目 3</div>
              </div>
            </div>
          </div>
        );
      
      case 'hover-click':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="relative">
              <div className="bg-orange-500 text-white px-4 py-2 rounded">親メニュー</div>
              <div className="absolute left-full top-0 ml-2 bg-orange-400 text-white px-4 py-2 rounded">
                サブメニュー
              </div>
            </div>
          </div>
        );
      
      case 'nested-hover':
        return (
          <div className={`${commonStyles} flex items-center justify-center gap-2`}>
            <div className="bg-pink-500 text-white px-3 py-2 rounded">Lv1</div>
            <div className="text-gray-400">→</div>
            <div className="bg-pink-400 text-white px-3 py-2 rounded">Lv2</div>
            <div className="text-gray-400">→</div>
            <div className="bg-pink-300 text-white px-3 py-2 rounded">Lv3</div>
          </div>
        );
      
      case 'image-preview':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="relative">
              <div className="w-20 h-20 bg-gray-300 rounded border-2 flex items-center justify-center text-3xl">
                📷
              </div>
              <div className="absolute -top-4 -right-4 w-32 h-32 bg-blue-200 rounded shadow-xl border-2 border-blue-400 flex items-center justify-center text-2xl">
                🖼️
              </div>
            </div>
          </div>
        );
      
      case 'drag-basic':
        return (
          <div className={`${commonStyles} flex items-center justify-around px-12`}>
            <div className="bg-blue-500 w-24 h-24 rounded shadow-lg flex items-center justify-center text-white font-bold text-sm text-center">
              ドラッグ元
            </div>
            <Move className="text-gray-500" size={40} />
            <div className="border-4 border-dashed border-green-500 w-24 h-24 rounded flex items-center justify-center text-green-600 font-bold text-sm text-center">
              ドロップ先
            </div>
          </div>
        );
      
      case 'drag-offset':
        return (
          <div className={`${commonStyles} relative overflow-hidden`}>
            <div className="absolute top-16 left-12 bg-red-500 w-16 h-16 rounded shadow-lg"></div>
            <div className="absolute bg-red-300 w-16 h-16 rounded shadow-lg opacity-50" style={{top: '64px', left: '148px'}}></div>
            <div className="absolute text-xs text-gray-700 bg-white px-2 py-1 rounded shadow" style={{top: '110px', left: '80px'}}>
              +100px, +50px
            </div>
          </div>
        );
      
      case 'slider-drag':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="w-64">
              <div className="relative h-2 bg-gray-300 rounded-full">
                <div className="absolute h-2 bg-blue-500 rounded-full" style={{width: '50%'}}></div>
                <div className="absolute w-6 h-6 bg-blue-600 rounded-full shadow-lg cursor-pointer" style={{left: '50%', top: '-8px', transform: 'translateX(-50%)'}}></div>
              </div>
            </div>
          </div>
        );
      
      case 'sortable-list':
        return (
          <div className={`${commonStyles} flex flex-col items-center justify-center gap-2 p-4`}>
            {['項目 1', '項目 2', '項目 3'].map((item, i) => (
              <div key={i} className="bg-purple-100 border-2 border-purple-300 w-48 px-4 py-2 rounded cursor-move flex items-center gap-2">
                <span className="text-gray-500">☰</span>
                {item}
              </div>
            ))}
          </div>
        );
      
      case 'mouse-trail':
        return (
          <div className={`${commonStyles} relative flex items-center justify-center`}>
            <svg className="w-32 h-32">
              <circle cx="64" cy="64" r="50" fill="none" stroke="#3B82F6" strokeWidth="3" strokeDasharray="5,5" />
            </svg>
            <div className="absolute text-gray-600 text-sm">
              描画エリア
            </div>
          </div>
        );
      
      case 'scroll':
        return (
          <div className={`${commonStyles} overflow-hidden relative`}>
            <div className="h-96 bg-gradient-to-b from-blue-100 via-blue-200 to-blue-300 p-4 space-y-2">
              <div className="bg-white p-2 rounded shadow">コンテンツ 1</div>
              <div className="bg-white p-2 rounded shadow">コンテンツ 2</div>
              <div className="bg-white p-2 rounded shadow">コンテンツ 3</div>
              <div className="bg-white p-2 rounded shadow">コンテンツ 4</div>
            </div>
            <div className="absolute bottom-4 right-4 bg-gray-800 bg-opacity-70 text-white px-3 py-1 rounded text-xs">
              ↕ スクロール
            </div>
          </div>
        );
      
      case 'long-press':
        return (
          <div className={`${commonStyles} flex items-center justify-center`}>
            <div className="relative">
              <button className="bg-teal-500 text-white font-bold py-3 px-6 rounded-lg">
                長押し
              </button>
              <div className="absolute -top-10 left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs px-3 py-1 rounded whitespace-nowrap">
                2秒間押し続ける
              </div>
            </div>
          </div>
        );
      
      case 'mouse-out':
        return (
          <div className={`${commonStyles} flex items-center justify-center gap-8`}>
            <div className="bg-red-400 w-24 h-24 rounded flex items-center justify-center text-white font-bold text-sm text-center">
              ホバー<br/>領域
            </div>
            <div className="text-gray-400 text-3xl">→</div>
            <div className="bg-gray-300 w-24 h-24 rounded flex items-center justify-center text-gray-600 font-bold">
              外側
            </div>
          </div>
        );
      
      default:
        return <div className={commonStyles}></div>;
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
          <Mouse className="text-blue-600" size={40} />
          Selenium マウス操作完全ガイド
        </h1>
        <p className="text-gray-600 text-lg">
          ActionChainsを使った全てのマウス操作パターン
        </p>
      </div>

      <div className="flex flex-wrap gap-2 mb-6 border-b-2 bg-white rounded-t-lg p-2">
        {[
          { id: 'click', label: 'クリック操作', icon: Hand },
          { id: 'hover', label: 'ホバー操作', icon: Target },
          { id: 'drag', label: 'ドラッグ操作', icon: Move },
          { id: 'advanced', label: '高度な操作', icon: ZoomIn },
          { id: 'chain', label: '複合操作', icon: Mouse }
        ].map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-3 font-medium transition-all rounded-lg flex items-center gap-2 ${
              activeTab === tab.id
                ? 'text-white bg-gradient-to-r from-blue-600 to-purple-600 shadow-lg'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <tab.icon size={18} />
            {tab.label}
          </button>
        ))}
      </div>

      <div className="space-y-6">
        {examples[activeTab].map((example, index) => (
          <div
            key={index}
            className="border-2 border-blue-200 rounded-xl p-6 bg-white hover:shadow-2xl transition-all duration-300"
          >
            <div className="flex items-start gap-3 mb-4">
              <div className="bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold text-lg shadow-lg">
                {index + 1}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mt-1">
                {example.title}
              </h3>
            </div>

            {example.visual && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <Mouse size={18} className="text-purple-600" />
                  ビジュアル図解
                </div>
                <DemoBox type={example.visual} />
              </div>
            )}

            <div className="mb-4">
              <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <Target size={18} className="text-blue-600" />
                Python コード
              </div>
              <pre className="bg-gray-900 text-green-300 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                <code>{example.python}</code>
              </pre>
            </div>

            <div className="flex items-start gap-3 bg-gradient-to-r from-blue-50 to-purple-50 p-4 rounded-lg border-l-4 border-blue-400">
              <Lightbulb className="text-blue-600 mt-0.5 flex-shrink-0" size={20} />
              <p className="text-gray-700 font-medium">{example.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 p-6 bg-white border-l-4 border-purple-500 rounded-lg shadow-md">
        <h4 className="font-bold text-gray-800 mb-4 text-xl flex items-center gap-2">
          <Lightbulb className="text-purple-600" />
          マウス操作の重要ポイント
        </h4>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div className="bg-blue-50 p-4 rounded-lg">
            <strong className="text-blue-700 text-base">ActionChains の基本</strong>
            <p className="mt-2">全てのマウス操作は ActionChains クラスを使用し、最後に .perform() を呼ぶ</p>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <strong className="text-purple-700 text-base">チェーン可能</strong>
            <p className="mt-2">複数の操作をドットで繋げて一連の動作として実行できる</p>
          </div>
          <div className="bg-pink-50 p-4 rounded-lg">
            <strong className="text-pink-700 text-base">待機処理</strong>
            <p className="mt-2">ホバーやドラッグの後は .pause() で待機時間を追加</p>
          </div>
          <div className="bg-indigo-50 p-4 rounded-lg">
            <strong className="text-indigo-700 text-base">エラー対策</strong>
            <p className="mt-2">要素が画面外の場合は scrollIntoView() でスクロールしてから操作</p>
          </div>
        </div>
      </div>

      <div className="mt-6 p-6 bg-gradient-to-r from-yellow-50 to-orange-50 border-l-4 border-yellow-500 rounded-lg">
        <h4 className="font-bold text-gray-800 mb-3 text-lg flex items-center gap-2">
          💡 よくあるマウス操作のパターン
        </h4>
        <div className="space-y-3 text-sm">
          <div className="bg-white p-3 rounded shadow-sm">
            <strong className="text-gray-800">クリック系:</strong>
            <span className="text-gray-600 ml-2">click(), double_click(), context_click()</span>
          </div>
          <div className="bg-white p-3 rounded shadow-sm">
            <strong className="text-gray-800">移動系:</strong>
            <span className="text-gray-600 ml-2">move_to_element(), move_by_offset(), move_to_element_with_offset()</span>
          </div>
          <div className="bg-white p-3 rounded shadow-sm">
            <strong className="text-gray-800">ドラッグ系:</strong>
            <span className="text-gray-600 ml-2">drag_and_drop(), click_and_hold(), release()</span>
          </div>
          <div className="bg-white p-3 rounded shadow-sm">
            <strong className="text-gray-800">制御系:</strong>
            <span className="text-gray-600 ml-2">pause(), key_down(), key_up()</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeleniumMouseOps;