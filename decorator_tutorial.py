# ============================================
# Pythonデコレーター完全解説 - 新人エンジニア向け
# ============================================

import time  # 時間計測用
from functools import wraps  # デコレーターを作る時の必須ツール
from typing import Callable, Any  # 型ヒント用


# ============================================
# 【基礎編】デコレーターとは？
# ============================================

print("=" * 60)
print("【1】デコレーターの基本概念")
print("=" * 60)

# デコレーターは「関数を装飾(デコレート)する関数」
# つまり、既存の関数に機能を追加するラッパー(包み)のようなもの

# まずはデコレーターなしで書いてみる
def say_hello():
    """普通の関数"""
    print("こんにちは！")

say_hello()  # こんにちは！


# 次に、この関数の前後に処理を追加したい場合...
def say_hello_with_decoration():
    """手動で装飾した関数"""
    print("--- 開始 ---")  # 前処理
    print("こんにちは！")  # 本来の処理
    print("--- 終了 ---")  # 後処理

say_hello_with_decoration()


# でも毎回こう書くのは面倒... そこでデコレーター！


# ============================================
# 【実践1】最もシンプルなデコレーター
# ============================================

print("\n" + "=" * 60)
print("【2】最もシンプルなデコレーター")
print("=" * 60)

def my_decorator(func):
    """
    デコレーター関数
    
    Args:
        func: 装飾したい関数
        
    Returns:
        wrapper: 装飾された新しい関数
    """
    def wrapper():
        """ラッパー関数 - 元の関数を包む"""
        print("--- 開始 ---")  # 前処理
        func()  # 元の関数を実行
        print("--- 終了 ---")  # 後処理
    return wrapper  # ラッパー関数を返す


# デコレーターの使い方1: 手動で適用
def greet():
    print("おはよう！")

# 関数をデコレーターに渡す
decorated_greet = my_decorator(greet)
decorated_greet()


# デコレーターの使い方2: @記法（これが一般的！）
@my_decorator  # この1行で上記と同じことができる
def say_goodbye():
    print("さようなら！")

say_goodbye()  # 自動的に装飾される


# ============================================
# 【実践2】引数を持つ関数をデコレートする
# ============================================

print("\n" + "=" * 60)
print("【3】引数を持つ関数のデコレート")
print("=" * 60)

def smart_decorator(func):
    """
    引数を受け取れるデコレーター
    *args, **kwargs を使って任意の引数に対応
    """
    @wraps(func)  # 元の関数の情報(名前、docstring等)を保持する
    def wrapper(*args, **kwargs):
        """
        *args: 位置引数をタプルで受け取る
        **kwargs: キーワード引数を辞書で受け取る
        """
        print(f"[DEBUG] 関数 '{func.__name__}' を実行します")
        print(f"[DEBUG] 引数: args={args}, kwargs={kwargs}")
        
        result = func(*args, **kwargs)  # 元の関数を実行して結果を受け取る
        
        print(f"[DEBUG] 関数 '{func.__name__}' が終了しました")
        print(f"[DEBUG] 戻り値: {result}")
        return result  # 結果を返す
    return wrapper


@smart_decorator
def add(a, b):
    """2つの数を足す関数"""
    return a + b


@smart_decorator
def greet_person(name, greeting="こんにちは"):
    """挨拶する関数"""
    message = f"{greeting}、{name}さん！"
    print(message)
    return message


# 実行
print("\n--- add関数の実行 ---")
result = add(5, 3)

print("\n--- greet_person関数の実行 ---")
result = greet_person("田中", greeting="おはよう")


# ============================================
# 【実践3】実用的なデコレーター例
# ============================================

print("\n" + "=" * 60)
print("【4】実用的なデコレーター集")
print("=" * 60)

# --- 3-1. 実行時間を計測するデコレーター ---
def timer(func):
    """関数の実行時間を計測するデコレーター"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # 開始時刻を記録
        result = func(*args, **kwargs)  # 関数を実行
        end_time = time.time()  # 終了時刻を記録
        elapsed = end_time - start_time  # 経過時間を計算
        print(f"⏱️  {func.__name__}の実行時間: {elapsed:.4f}秒")
        return result
    return wrapper


@timer
def slow_function():
    """重い処理をシミュレート"""
    print("処理中...")
    time.sleep(1)  # 1秒待つ
    print("処理完了！")


print("\n--- 実行時間計測 ---")
slow_function()


# --- 3-2. リトライ機能を追加するデコレーター ---
def retry(max_attempts=3):
    """
    失敗時に自動でリトライするデコレーター
    これは「引数を持つデコレーター」の例
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    print(f"🔄 試行 {attempt}/{max_attempts}")
                    result = func(*args, **kwargs)
                    print(f"✅ 成功！")
                    return result
                except Exception as e:
                    print(f"❌ エラー: {e}")
                    if attempt == max_attempts:
                        print(f"⛔ {max_attempts}回試行しましたが失敗しました")
                        raise  # 最後の試行で失敗したら例外を投げる
                    time.sleep(0.5)  # 少し待ってからリトライ
        return wrapper
    return decorator


# 使用例: 最大3回までリトライ
attempt_count = 0

@retry(max_attempts=3)
def unstable_function():
    """時々失敗する関数（デモ用）"""
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:  # 3回目で成功する
        raise ValueError("まだ失敗するよ！")
    return "成功しました！"


print("\n--- リトライ機能のテスト ---")
try:
    result = unstable_function()
    print(f"結果: {result}")
except Exception as e:
    print(f"最終的にエラー: {e}")

attempt_count = 0  # カウンターをリセット


# --- 3-3. ログを出力するデコレーター ---
def log_function_call(func):
    """関数の呼び出しをログに記録するデコレーター"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 引数を見やすくフォーマット
        args_str = ", ".join([repr(a) for a in args])
        kwargs_str = ", ".join([f"{k}={v!r}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        print(f"📝 LOG: {func.__name__}({all_args}) を呼び出しました")
        result = func(*args, **kwargs)
        print(f"📝 LOG: {func.__name__} が {result!r} を返しました")
        return result
    return wrapper


@log_function_call
def calculate(x, y, operation="add"):
    """計算を行う関数"""
    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    else:
        return None


print("\n--- ログ機能のテスト ---")
calculate(10, 5)
calculate(10, 5, operation="multiply")


# --- 3-4. 結果をキャッシュするデコレーター ---
def cache(func):
    """
    関数の結果をキャッシュして、同じ引数の場合は再計算しない
    メモ化(memoization)とも呼ばれる
    """
    cached_results = {}  # キャッシュを保存する辞書
    
    @wraps(func)
    def wrapper(*args):
        if args in cached_results:  # キャッシュに結果がある場合
            print(f"💾 キャッシュから取得: {args}")
            return cached_results[args]
        
        print(f"🔄 計算中: {args}")
        result = func(*args)  # 関数を実行
        cached_results[args] = result  # 結果をキャッシュに保存
        return result
    return wrapper


@cache
def fibonacci(n):
    """フィボナッチ数列（再帰版）"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


print("\n--- キャッシュ機能のテスト ---")
print(f"fibonacci(5) = {fibonacci(5)}")
print(f"fibonacci(5) = {fibonacci(5)}")  # 2回目はキャッシュから取得


# ============================================
# 【実践4】複数のデコレーターを重ねる
# ============================================

print("\n" + "=" * 60)
print("【5】複数のデコレーターを組み合わせる")
print("=" * 60)

# デコレーターは複数重ねて使える
# 下から順に適用される（重要！）

@timer  # 2番目に適用される（外側）
@log_function_call  # 1番目に適用される（内側）
def complex_calculation(x, y):
    """複雑な計算（デモ用）"""
    time.sleep(0.5)  # 処理時間をシミュレート
    return x ** y


print("\n--- 複数デコレーターのテスト ---")
result = complex_calculation(2, 10)


# ============================================
# 【実践5】クラスメソッドのデコレーター
# ============================================

print("\n" + "=" * 60)
print("【6】クラスと一緒に使うデコレーター")
print("=" * 60)

class Student:
    """学生クラス"""
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @log_function_call  # インスタンスメソッドにも使える
    def introduce(self):
        """自己紹介"""
        return f"私は{self.name}、{self.age}歳です"
    
    @staticmethod
    @timer  # 静的メソッドにも使える
    def calculate_average(scores):
        """平均点を計算"""
        time.sleep(0.3)
        return sum(scores) / len(scores)
    
    @classmethod
    @log_function_call  # クラスメソッドにも使える
    def create_student(cls, name, age):
        """ファクトリーメソッド"""
        print(f"新しい学生を作成します")
        return cls(name, age)


print("\n--- クラスメソッドでのデコレーター ---")
student = Student("山田太郎", 20)
student.introduce()

print("\n--- 静的メソッドでのデコレーター ---")
avg = Student.calculate_average([80, 90, 85])
print(f"平均点: {avg}")

print("\n--- クラスメソッドでのデコレーター ---")
new_student = Student.create_student("佐藤花子", 19)


# ============================================
# 【実践6】引数を持つデコレーターの作り方
# ============================================

print("\n" + "=" * 60)
print("【7】引数を持つデコレーターの仕組み")
print("=" * 60)

def repeat(times=2):
    """
    関数を指定回数繰り返すデコレーター
    
    デコレーターに引数を渡す場合は、3階層の関数が必要:
    1. 外側: 引数を受け取る
    2. 中間: 関数を受け取る（実際のデコレーター）
    3. 内側: ラッパー関数
    """
    def decorator(func):  # 実際のデコレーター
        @wraps(func)
        def wrapper(*args, **kwargs):  # ラッパー
            results = []
            for i in range(times):
                print(f"--- {i + 1}回目 ---")
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return wrapper
    return decorator  # デコレーターを返す


@repeat(times=3)  # 3回繰り返す
def say_hello(name):
    """挨拶する"""
    message = f"こんにちは、{name}さん！"
    print(message)
    return message


print("\n--- 繰り返しデコレーター ---")
results = say_hello("田中")
print(f"\n全ての結果: {results}")


# ============================================
# 【まとめ】よく使う標準デコレーター
# ============================================

print("\n" + "=" * 60)
print("【8】Pythonの標準デコレーター")
print("=" * 60)

class Example:
    """標準デコレーターの例"""
    
    class_variable = "クラス変数"
    
    def __init__(self):
        self.instance_variable = "インスタンス変数"
    
    # @property - ゲッター（値を取得）
    @property
    def name(self):
        """プロパティ - メソッドを属性のように使える"""
        return "Example クラス"
    
    # @staticmethod - 静的メソッド（selfなし）
    @staticmethod
    def static_method():
        """静的メソッド - インスタンスに依存しない"""
        return "これは静的メソッドです"
    
    # @classmethod - クラスメソッド（clsを受け取る）
    @classmethod
    def class_method(cls):
        """クラスメソッド - クラス自体を操作"""
        return f"これは{cls.__name__}のクラスメソッドです"


print("\n--- 標準デコレーターの使用例 ---")
example = Example()
print(f"@property: {example.name}")  # メソッドだが()不要
print(f"@staticmethod: {Example.static_method()}")
print(f"@classmethod: {Example.class_method()}")


# ============================================
# 【終了】
# ============================================

print("\n" + "=" * 60)
print("デコレーター学習完了！🎉")
print("=" * 60)

print("""
【デコレーターのポイント】
✅ デコレーターは関数を装飾する関数
✅ @記法で簡単に適用できる
✅ @wraps(func)を使って元の情報を保持
✅ *args, **kwargsで任意の引数に対応
✅ 実行時間計測、ログ、キャッシュなどに便利
✅ 複数重ねることも可能
✅ 引数を持つ場合は3階層の関数が必要
""")