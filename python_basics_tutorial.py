# ============================================
# Python基礎学習プロジェクト - 新人エンジニア向け
# ============================================

# --- 1. モジュールのインポート ---
import logging  # ログ出力用の標準ライブラリ
from datetime import datetime  # 日時操作用
from typing import List, Optional  # 型ヒント用


# --- 2. ロギングの設定 ---
# ログの設定を行う(レベル、フォーマット、出力先を指定)
logging.basicConfig(
    level=logging.DEBUG,  # DEBUGレベル以上のログを出力
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # ログのフォーマット
    handlers=[
        logging.FileHandler('app.log'),  # ファイルに出力
        logging.StreamHandler()  # コンソールにも出力
    ]
)
# ロガーインスタンスを作成
logger = logging.getLogger(__name__)


# --- 3. クラスの定義 ---
class Student:
    """
    学生を表すクラス
    クラス変数とインスタンス変数、各種メソッドを持つ
    """
    
    # クラス変数(全インスタンスで共有される変数)
    school_name = "プログラミング学校"  # すべての学生が所属する学校名
    student_count = 0  # 学生の総数をカウント
    
    def __init__(self, name: str, age: int, grade: int):
        """
        コンストラクタ - インスタンス生成時に呼ばれる特殊メソッド
        
        Args:
            name: 学生の名前
            age: 学生の年齢
            grade: 学生の学年
        """
        # インスタンス変数(各インスタンス固有の変数)
        self.name = name  # 学生の名前を保存
        self.age = age  # 学生の年齢を保存
        self.grade = grade  # 学生の学年を保存
        self.scores: List[int] = []  # テストの点数リスト(初期は空)
        
        # クラス変数をインクリメント
        Student.student_count += 1  # 学生数を1増やす
        
        # デバッグプリント(開発時の動作確認用)
        print(f"[DEBUG] 新しい学生を作成: {self.name}")
        # ログ出力
        logger.info(f"学生インスタンス作成: {self.name}, 年齢: {self.age}")
    
    def add_score(self, score: int) -> None:
        """
        テストの点数を追加するメソッド
        
        Args:
            score: 追加する点数(0-100)
        """
        # 入力値の検証
        if not 0 <= score <= 100:  # scoreが0以上100以下でない場合
            logger.warning(f"無効な点数: {score}")  # 警告ログを出力
            raise ValueError("点数は0-100の範囲で指定してください")  # 例外を発生させる
        
        self.scores.append(score)  # スコアリストに追加
        print(f"[DEBUG] {self.name}の点数追加: {score}")  # デバッグプリント
        logger.debug(f"{self.name}のスコア追加: {score}")  # デバッグログ
    
    def get_average(self) -> Optional[float]:
        """
        平均点を計算して返すメソッド
        
        Returns:
            平均点(float) または スコアがない場合はNone
        """
        if not self.scores:  # スコアリストが空の場合
            logger.warning(f"{self.name}のスコアが未登録")  # 警告ログ
            return None  # Noneを返す
        
        average = sum(self.scores) / len(self.scores)  # 平均を計算
        logger.info(f"{self.name}の平均点: {average:.2f}")  # 情報ログ
        return average  # 平均点を返す
    
    def is_passing(self, passing_score: int = 60) -> bool:
        """
        合格判定を行うメソッド
        
        Args:
            passing_score: 合格基準点(デフォルト60点)
            
        Returns:
            合格ならTrue、不合格ならFalse
        """
        average = self.get_average()  # 平均点を取得
        if average is None:  # 平均点がNoneの場合
            return False  # 不合格とする
        return average >= passing_score  # 合格基準点以上ならTrue
    
    def __str__(self) -> str:
        """
        文字列表現を返す特殊メソッド(print時に呼ばれる)
        
        Returns:
            学生情報の文字列
        """
        avg = self.get_average()  # 平均点を取得
        avg_str = f"{avg:.2f}" if avg is not None else "未受験"  # 平均点の文字列
        return f"学生名: {self.name}, 年齢: {self.age}, 学年: {self.grade}, 平均点: {avg_str}"
    
    @classmethod
    def get_student_count(cls) -> int:
        """
        クラスメソッド - クラス変数にアクセスするメソッド
        
        Returns:
            現在の学生総数
        """
        logger.info(f"現在の学生総数: {cls.student_count}")  # 情報ログ
        return cls.student_count  # 学生数を返す
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """
        静的メソッド - インスタンスやクラスに依存しない処理
        
        Args:
            age: 検証する年齢
            
        Returns:
            有効な年齢ならTrue
        """
        return 0 < age < 150  # 年齢が1歳以上150歳未満ならTrue


# --- 4. 関数の定義 ---
def calculate_class_average(students: List[Student]) -> Optional[float]:
    """
    クラス全体の平均点を計算する関数
    
    Args:
        students: 学生オブジェクトのリスト
        
    Returns:
        クラス全体の平均点 または 学生がいない場合はNone
    """
    # デバッグプリント
    print(f"[DEBUG] クラス平均計算開始: {len(students)}人の学生")
    logger.debug(f"クラス平均計算: 学生数={len(students)}")  # デバッグログ
    
    if not students:  # 学生リストが空の場合
        logger.warning("学生が登録されていません")  # 警告ログ
        return None  # Noneを返す
    
    # すべての学生の平均点を集める
    averages = [s.get_average() for s in students if s.get_average() is not None]
    
    if not averages:  # 平均点が一つもない場合
        logger.warning("計算可能な平均点がありません")  # 警告ログ
        return None  # Noneを返す
    
    class_avg = sum(averages) / len(averages)  # クラス平均を計算
    logger.info(f"クラス平均点: {class_avg:.2f}")  # 情報ログ
    return class_avg  # クラス平均を返す


def find_top_student(students: List[Student]) -> Optional[Student]:
    """
    最高得点の学生を見つける関数
    
    Args:
        students: 学生オブジェクトのリスト
        
    Returns:
        最高得点の学生 または 該当者がいない場合はNone
    """
    # デバッグプリント
    print(f"[DEBUG] トップ学生検索開始")
    
    # 平均点がある学生のみをフィルタリング
    students_with_scores = [s for s in students if s.get_average() is not None]
    
    if not students_with_scores:  # 該当する学生がいない場合
        logger.warning("スコアを持つ学生がいません")  # 警告ログ
        return None  # Noneを返す
    
    # max関数でkeyに平均点を指定して最高得点者を取得
    top = max(students_with_scores, key=lambda s: s.get_average())
    logger.info(f"トップ学生: {top.name}, 平均: {top.get_average():.2f}")  # 情報ログ
    return top  # トップ学生を返す


# --- 5. メイン実行部分 ---
def main():
    """
    メイン関数 - プログラムのエントリーポイント
    """
    print("=" * 50)  # 区切り線
    print("Python基礎学習プログラム 実行開始")  # タイトル出力
    print("=" * 50)
    logger.info("プログラム開始")  # 開始ログ
    
    try:  # 例外処理のためのtryブロック
        # --- 学生インスタンスの作成 ---
        print("\n### 1. 学生インスタンスの作成 ###")
        student1 = Student("田中太郎", 20, 2)  # 1人目の学生を作成
        student2 = Student("佐藤花子", 19, 1)  # 2人目の学生を作成
        student3 = Student("鈴木一郎", 21, 3)  # 3人目の学生を作成
        
        # --- クラスメソッドの使用 ---
        print(f"\n現在の学生数: {Student.get_student_count()}人")  # クラスメソッド呼び出し
        
        # --- 点数の追加 ---
        print("\n### 2. テスト点数の追加 ###")
        student1.add_score(85)  # 田中さんに点数追加
        student1.add_score(90)  # 田中さんに点数追加
        student1.add_score(78)  # 田中さんに点数追加
        
        student2.add_score(92)  # 佐藤さんに点数追加
        student2.add_score(88)  # 佐藤さんに点数追加
        student2.add_score(95)  # 佐藤さんに点数追加
        
        student3.add_score(70)  # 鈴木さんに点数追加
        student3.add_score(75)  # 鈴木さんに点数追加
        
        # --- 学生情報の表示 ---
        print("\n### 3. 学生情報の表示 ###")
        students = [student1, student2, student3]  # 学生リストを作成
        for student in students:  # リストをループで処理
            print(student)  # __str__メソッドが呼ばれる
            passing = "合格" if student.is_passing() else "不合格"  # 三項演算子
            print(f"  → 判定: {passing}\n")  # 合格判定結果を表示
        
        # --- クラス平均の計算 ---
        print("### 4. クラス全体の統計 ###")
        class_avg = calculate_class_average(students)  # 関数を呼び出し
        if class_avg:  # class_avgがNoneでない場合
            print(f"クラス平均点: {class_avg:.2f}点")  # 平均点を表示
        
        # --- トップ学生の検索 ---
        top_student = find_top_student(students)  # 関数を呼び出し
        if top_student:  # top_studentがNoneでない場合
            print(f"トップ学生: {top_student.name} ({top_student.get_average():.2f}点)")
        
        # --- 静的メソッドの使用 ---
        print("\n### 5. 静的メソッドのテスト ###")
        test_age = 25  # テスト用の年齢
        if Student.validate_age(test_age):  # 静的メソッド呼び出し
            print(f"年齢{test_age}歳は有効です")  # 有効な場合
        
        # --- エラーハンドリングのテスト ---
        print("\n### 6. エラーハンドリングのテスト ###")
        try:  # ネストしたtryブロック
            student1.add_score(150)  # 無効な点数を追加(エラーが発生)
        except ValueError as e:  # ValueErrorをキャッチ
            print(f"エラーをキャッチ: {e}")  # エラーメッセージを表示
            logger.error(f"入力エラー: {e}")  # エラーログ
        
        # --- リスト内包表記の例 ---
        print("\n### 7. リスト内包表記の例 ###")
        # 合格者のみをフィルタリング
        passing_students = [s.name for s in students if s.is_passing()]
        print(f"合格者: {', '.join(passing_students)}")  # 合格者名を表示
        
        # --- 辞書の使用例 ---
        print("\n### 8. 辞書の使用例 ###")
        # 学生名をキー、平均点を値とする辞書を作成
        score_dict = {s.name: s.get_average() for s in students if s.get_average()}
        for name, avg in score_dict.items():  # 辞書をループ
            print(f"{name}: {avg:.2f}点")  # 名前と平均点を表示
        
    except Exception as e:  # すべての例外をキャッチ
        print(f"\n予期しないエラーが発生: {e}")  # エラーメッセージ表示
        logger.error(f"予期しないエラー: {e}", exc_info=True)  # エラーログ(トレースバック付き)
    
    finally:  # 例外の有無に関わらず必ず実行される
        print("\n" + "=" * 50)  # 区切り線
        print("プログラム終了")  # 終了メッセージ
        print("=" * 50)
        logger.info("プログラム終了")  # 終了ログ


# --- 6. エントリーポイント ---
if __name__ == "__main__":  # このファイルが直接実行された場合のみ
    main()  # main関数を呼び出す