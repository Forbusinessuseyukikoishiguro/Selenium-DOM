import React, { useState } from 'react';
import { MousePointer, Move, Target, Lightbulb } from 'lucide-react';

const SeleniumCoordinates = () => {
  const [activeTab, setActiveTab] = useState('basic');
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  const examples = {
    basic: [
      {
        title: '要素の座標を取得',
        visual: 'element-location',
        python: `# 要素の位置（左上座標）を取得
element = driver.find_element(By.ID, "target-button")
location = element.location

print(f"X座標: {location['x']}")
print(f"Y座標: {location['y']}")

# 要素のサイズを取得
size = element.size
print(f"幅: {size['width']}")
print(f"高さ: {size['height']}")

# 中心座標を計算
center_x = location['x'] + size['width'] / 2
center_y = location['y'] + size['height'] / 2`,
        desc: '要素の位置とサイズから座標を取得'
      },
      {
        title: '絶対座標でクリック',
        visual: 'absolute-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# ActionChainsを使用
actions = ActionChains(driver)

# 画面の絶対座標(x=300, y=400)をクリック
actions.move_by_offset(300, 400).click().perform()

# クリック後はオフセットをリセット
actions.move_by_offset(-300, -400).perform()`,
        desc: '画面上の絶対座標位置をクリック'
      },
      {
        title: '要素からの相対座標でクリック',
        visual: 'relative-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.ID, "base-element")
actions = ActionChains(driver)

# 要素の中心から右に50px、下に30pxの位置をクリック
actions.move_to_element_with_offset(
    element, 
    50,      # X方向のオフセット
    30       # Y方向のオフセット
).click().perform()`,
        desc: '要素を基準とした相対座標でクリック'
      },
      {
        title: '要素の中心をクリック',
        visual: 'center-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.CLASS_NAME, "target")
actions = ActionChains(driver)

# 要素の中心に移動してクリック
actions.move_to_element(element).click().perform()

# または直接クリック
element.click()`,
        desc: '要素の中心位置を自動計算してクリック'
      }
    ],
    advanced: [
      {
        title: 'ドラッグ&ドロップ（座標指定）',
        visual: 'drag-drop',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# 要素を取得
draggable = driver.find_element(By.ID, "draggable")
actions = ActionChains(driver)

# 要素を右に200px、下に100px移動
actions.click_and_hold(draggable)\\
    .move_by_offset(200, 100)\\
    .release()\\
    .perform()

# または要素間のドラッグ&ドロップ
source = driver.find_element(By.ID, "source")
target = driver.find_element(By.ID, "target")
actions.drag_and_drop(source, target).perform()`,
        desc: '要素を座標指定でドラッグ移動'
      },
      {
        title: '複数ポイントの順次クリック',
        visual: 'multi-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains
import time

actions = ActionChains(driver)

# 複数の座標を順番にクリック
coordinates = [
    (100, 150),
    (200, 150),
    (300, 150),
    (400, 150)
]

for x, y in coordinates:
    actions.move_by_offset(x, y).click().perform()
    # オフセットをリセット
    actions.move_by_offset(-x, -y).perform()
    time.sleep(0.5)`,
        desc: '複数の座標を連続してクリック'
      },
      {
        title: 'マウスホバー（特定位置）',
        visual: 'hover',
        python: `from selenium.webdriver.common.action_chains import ActionChains

element = driver.find_element(By.CLASS_NAME, "menu-item")
actions = ActionChains(driver)

# 要素の特定位置にホバー
actions.move_to_element_with_offset(
    element,
    10,   # 左端から10px
    10    # 上端から10px
).perform()

# ホバーメニューが表示されるまで待機
time.sleep(1)

# サブメニューをクリック
submenu = driver.find_element(By.CLASS_NAME, "submenu-item")
submenu.click()`,
        desc: '要素の特定位置にマウスホバー'
      },
      {
        title: 'スクロールと座標の組み合わせ',
        visual: 'scroll-click',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# 特定の座標までスクロール
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(1)

# スクロール後の座標でクリック
actions = ActionChains(driver)
actions.move_by_offset(300, 200).click().perform()

# または要素までスクロールしてからクリック
element = driver.find_element(By.ID, "bottom-button")
driver.execute_script(
    "arguments[0].scrollIntoView(true);", 
    element
)
time.sleep(0.5)
element.click()`,
        desc: 'スクロール後の座標を考慮した操作'
      }
    ],
    practical: [
      {
        title: 'キャンバス上の描画',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# キャンバス要素を取得
canvas = driver.find_element(By.ID, "drawing-canvas")
actions = ActionChains(driver)

# キャンバス上に線を描く
actions.move_to_element_with_offset(canvas, 10, 10)\\
    .click_and_hold()\\
    .move_by_offset(100, 0)\\
    .move_by_offset(0, 100)\\
    .move_by_offset(-100, 0)\\
    .move_by_offset(0, -100)\\
    .release()\\
    .perform()`,
        desc: 'HTML5キャンバスに座標で描画'
      },
      {
        title: 'スライダーの操作',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# スライダーを取得
slider = driver.find_element(By.CLASS_NAME, "slider-handle")
actions = ActionChains(driver)

# スライダーを右に150px移動
actions.click_and_hold(slider)\\
    .move_by_offset(150, 0)\\
    .release()\\
    .perform()

# または特定の値まで移動
slider_track = driver.find_element(By.CLASS_NAME, "slider-track")
track_width = slider_track.size['width']

# 50%の位置に移動（トラックの中央）
target_offset = track_width * 0.5
actions.click_and_hold(slider)\\
    .move_by_offset(target_offset, 0)\\
    .release()\\
    .perform()`,
        desc: 'レンジスライダーを座標で操作'
      },
      {
        title: '画像の特定部分をクリック',
        python: `from selenium.webdriver.common.action_chains import ActionChains

# 画像要素を取得
image = driver.find_element(By.ID, "map-image")
actions = ActionChains(driver)

# 画像の左上から30%, 40%の位置をクリック
image_width = image.size['width']
image_height = image.size['height']

# 画像の左上を基準に計算
offset_x = image_width * 0.3
offset_y = image_height * 0.4

# 画像の中心を基準とする場合
center_offset_x = offset_x - image_width / 2
center_offset_y = offset_y - image_height / 2

actions.move_to_element_with_offset(
    image,
    center_offset_x,
    center_offset_y
).click().perform()`,
        desc: '画像の特定部分を割合で指定してクリック'
      },
      {
        title: 'マウスジェスチャー',
        python: `from selenium.webdriver.common.action_chains import ActionChains
import time

actions = ActionChains(driver)

# 「Z」の字を描くジェスチャー
def draw_z_gesture(element):
    actions.move_to_element(element)\\
        .click_and_hold()\\
        .move_by_offset(100, 0)\\
        .move_by_offset(-100, 100)\\
        .move_by_offset(100, 0)\\
        .release()\\
        .perform()

# 円を描くジェスチャー
import math

def draw_circle_gesture(element, radius=50):
    actions.move_to_element(element).click_and_hold()
    
    for angle in range(0, 360, 10):
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        actions.move_by_offset(x, y)
    
    actions.release().perform()

canvas = driver.find_element(By.ID, "gesture-area")
draw_circle_gesture(canvas, radius=80)`,
        desc: '複雑なマウスジェスチャーの実装'
      }
    ]
  };

  const DemoBox = ({ type }) => {
    if (type === 'element-location') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-center">
          <div className="relative bg-blue-500 w-32 h-20 rounded shadow-lg flex items-center justify-center text-white font-bold">
            要素
            <div className="absolute -top-6 -left-6 text-xs text-gray-700 bg-yellow-200 px-2 py-1 rounded">
              (x, y)
            </div>
            <div className="absolute -bottom-6 -right-6 text-xs text-gray-700 bg-green-200 px-2 py-1 rounded">
              幅 × 高さ
            </div>
          </div>
        </div>
      );
    }
    
    if (type === 'absolute-click') {
      return (
        <div 
          className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 cursor-crosshair"
          onMouseMove={(e) => {
            const rect = e.currentTarget.getBoundingClientRect();
            setMousePos({ 
              x: Math.round(e.clientX - rect.left), 
              y: Math.round(e.clientY - rect.top) 
            });
          }}
        >
          <div className="absolute top-2 left-2 text-xs bg-white px-2 py-1 rounded shadow">
            マウス座標: ({mousePos.x}, {mousePos.y})
          </div>
          <Target className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-red-500" size={32} />
        </div>
      );
    }

    if (type === 'relative-click') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-center">
          <div className="relative bg-blue-500 w-32 h-20 rounded shadow-lg flex items-center justify-center text-white font-bold">
            基準要素
            <div className="absolute top-4 left-36 w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
              <MousePointer size={16} className="text-white" />
            </div>
            <div className="absolute top-6 left-32 text-xs bg-yellow-200 px-2 py-1 rounded text-gray-800">
              +50, +30
            </div>
          </div>
        </div>
      );
    }

    if (type === 'center-click') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-center">
          <div className="relative bg-green-500 w-32 h-20 rounded shadow-lg flex items-center justify-center text-white font-bold">
            <Target size={24} className="absolute text-white opacity-50" />
            中心
          </div>
        </div>
      );
    }

    if (type === 'drag-drop') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-center">
          <div className="bg-purple-500 w-24 h-24 rounded shadow-lg flex items-center justify-center text-white font-bold">
            開始
          </div>
          <Move className="mx-4 text-gray-600" size={32} />
          <div className="bg-pink-500 w-24 h-24 rounded shadow-lg flex items-center justify-center text-white font-bold">
            終了
          </div>
        </div>
      );
    }

    if (type === 'multi-click') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-around px-8">
          {[1, 2, 3, 4].map((num) => (
            <div key={num} className="relative">
              <div className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center text-white font-bold shadow-lg">
                {num}
              </div>
            </div>
          ))}
        </div>
      );
    }

    if (type === 'hover') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 flex items-center justify-center">
          <div className="relative bg-indigo-500 w-40 h-16 rounded shadow-lg flex items-center justify-center text-white font-bold">
            メニュー
            <MousePointer className="absolute -top-2 -left-2 text-yellow-400" size={20} />
          </div>
        </div>
      );
    }

    if (type === 'scroll-click') {
      return (
        <div className="relative bg-gray-100 h-48 rounded border-2 border-gray-300 overflow-hidden">
          <div className="h-96 bg-gradient-to-b from-blue-100 to-blue-300 p-4">
            <div className="bg-white p-4 rounded shadow mb-4">上部コンテンツ</div>
            <div className="bg-white p-4 rounded shadow mb-4">中部コンテンツ</div>
            <div className="bg-yellow-400 p-4 rounded shadow mb-4 font-bold">
              ← スクロール後にクリック
            </div>
          </div>
        </div>
      );
    }

    return null;
  };

  return (
    <div className="w-full max-w-6xl mx-auto p-6 bg-gradient-to-br from-purple-50 to-pink-50 min-h-screen">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-2 flex items-center gap-3">
          <MousePointer className="text-purple-600" />
          Selenium 座標指定ガイド
        </h1>
        <p className="text-gray-600 text-lg">
          座標を使った要素操作とActionChainsの活用方法
        </p>
      </div>

      <div className="flex flex-wrap gap-2 mb-6 border-b-2 bg-white rounded-t-lg p-2">
        <button
          onClick={() => setActiveTab('basic')}
          className={`px-6 py-3 font-medium transition-all rounded-lg ${
            activeTab === 'basic'
              ? 'text-white bg-purple-600 shadow-md'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          基本的な座標操作
        </button>
        <button
          onClick={() => setActiveTab('advanced')}
          className={`px-6 py-3 font-medium transition-all rounded-lg ${
            activeTab === 'advanced'
              ? 'text-white bg-purple-600 shadow-md'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          高度な座標操作
        </button>
        <button
          onClick={() => setActiveTab('practical')}
          className={`px-6 py-3 font-medium transition-all rounded-lg ${
            activeTab === 'practical'
              ? 'text-white bg-purple-600 shadow-md'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          実践的な応用例
        </button>
      </div>

      <div className="space-y-6">
        {examples[activeTab].map((example, index) => (
          <div
            key={index}
            className="border-2 border-purple-200 rounded-xl p-6 bg-white hover:shadow-xl transition-all duration-300"
          >
            <div className="flex items-start gap-3 mb-4">
              <div className="bg-gradient-to-br from-purple-500 to-pink-600 text-white w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 font-bold text-lg shadow-md">
                {index + 1}
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mt-1">
                {example.title}
              </h3>
            </div>

            {example.visual && (
              <div className="mb-4">
                <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                  <Target size={18} className="text-purple-600" />
                  ビジュアル図解
                </div>
                <DemoBox type={example.visual} />
              </div>
            )}

            <div className="mb-4">
              <div className="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
                <MousePointer size={18} className="text-pink-600" />
                Python コード
              </div>
              <pre className="bg-gray-900 text-green-300 p-4 rounded-lg text-sm overflow-x-auto font-mono">
                <code>{example.python}</code>
              </pre>
            </div>

            <div className="flex items-start gap-3 bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-lg border-l-4 border-purple-400">
              <Lightbulb className="text-purple-600 mt-0.5 flex-shrink-0" size={20} />
              <p className="text-gray-700 font-medium">{example.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 p-6 bg-white border-l-4 border-purple-500 rounded-lg shadow-md">
        <h4 className="font-bold text-gray-800 mb-4 text-xl flex items-center gap-2">
          <Lightbulb className="text-purple-600" />
          座標指定の重要ポイント
        </h4>
        <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-700">
          <div className="bg-purple-50 p-3 rounded">
            <strong className="text-purple-700">ActionChains必須</strong>
            <p className="mt-1">座標指定の操作には ActionChains クラスが必要</p>
          </div>
          <div className="bg-pink-50 p-3 rounded">
            <strong className="text-pink-700">オフセットのリセット</strong>
            <p className="mt-1">move_by_offset 後は逆方向に移動してリセット</p>
          </div>
          <div className="bg-indigo-50 p-3 rounded">
            <strong className="text-indigo-700">相対座標が便利</strong>
            <p className="mt-1">要素基準の相対座標は画面サイズに依存しない</p>
          </div>
          <div className="bg-blue-50 p-3 rounded">
            <strong className="text-blue-700">スクロール考慮</strong>
            <p className="mt-1">ページスクロール後は座標がずれる可能性あり</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeleniumCoordinates;