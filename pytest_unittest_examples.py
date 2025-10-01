# ============================================
# テストコード - pytest & unittest の例
# ============================================

# --- pytest用テストコード ---
# ファイル名: test_student_pytest.py

import pytest  # pytestフレームワークをインポート
from python_basics_tutorial import Student, calculate_class_average, find_top_student


# --- フィクスチャ(テスト用のデータを準備する機能) ---
@pytest.fixture
def sample_student():
    """
    テスト用の学生インスタンスを返すフィクスチャ
    各テスト関数の前に自動的に実行される
    """
    return Student("テスト太郎", 20, 2)  # テスト用学生を作成して返す


@pytest.fixture
def students_with_scores():
    """
    複数の学生と点数を持つフィクスチャ
    """
    s1 = Student("学生A", 20, 2)  # 学生Aを作成
    s1.add_score(80)  # 点数追加
    s1.add_score(85)  # 点数追加
    
    s2 = Student("学生B", 19, 1)  # 学生Bを作成
    s2.add_score(90)  # 点数追加
    s2.add_score(95)  # 点数追加
    
    return [s1, s2]  # 学生リストを返す


# --- 基本的なテストケース ---
def test_student_creation(sample_student):
    """
    学生インスタンスが正しく作成されるかテスト
    
    Args:
        sample_student: フィクスチャから渡される学生インスタンス
    """
    # アサーション(検証)
    assert sample_student.name == "テスト太郎"  # 名前が正しいか
    assert sample_student.age == 20  # 年齢が正しいか
    assert sample_student.grade == 2  # 学年が正しいか
    assert sample_student.scores == []  # 初期スコアが空リストか


def test_add_score_valid(sample_student):
    """
    有効な点数が正しく追加されるかテスト
    """
    sample_student.add_score(85)  # 点数を追加
    assert len(sample_student.scores) == 1  # リストの長さが1か
    assert sample_student.scores[0] == 85  # 追加した点数が正しいか


def test_add_score_invalid(sample_student):
    """
    無効な点数を追加するとエラーが発生するかテスト
    """
    # pytest.raisesで例外が発生することを検証
    with pytest.raises(ValueError):  # ValueErrorが発生することを期待
        sample_student.add_score(150)  # 無効な点数(100超)を追加
    
    with pytest.raises(ValueError):  # ValueErrorが発生することを期待
        sample_student.add_score(-10)  # 無効な点数(負数)を追加


def test_get_average_no_scores(sample_student):
    """
    スコアがない場合、平均がNoneになるかテスト
    """
    assert sample_student.get_average() is None  # Noneが返されるか


def test_get_average_with_scores(sample_student):
    """
    スコアがある場合、正しい平均が計算されるかテスト
    """
    sample_student.add_score(80)  # 点数追加
    sample_student.add_score(90)  # 点数追加
    sample_student.add_score(70)  # 点数追加
    
    average = sample_student.get_average()  # 平均を取得
    assert average == 80.0  # (80+90+70)/3 = 80.0


def test_is_passing_with_scores(sample_student):
    """
    合格判定が正しく行われるかテスト
    """
    sample_student.add_score(70)  # 点数追加
    sample_student.add_score(80)  # 点数追加
    
    assert sample_student.is_passing() is True  # 平均75点なので合格(60点以上)
    assert sample_student.is_passing(80) is False  # 基準80点なら不合格


def test_calculate_class_average(students_with_scores):
    """
    クラス平均が正しく計算されるかテスト
    """
    class_avg = calculate_class_average(students_with_scores)  # クラス平均計算
    # 学生Aの平均: 82.5, 学生Bの平均: 92.5 → クラス平均: 87.5
    assert class_avg == 87.5


def test_calculate_class_average_empty():
    """
    学生がいない場合、Noneが返されるかテスト
    """
    assert calculate_class_average([]) is None  # 空リストでNone


def test_find_top_student(students_with_scores):
    """
    トップ学生が正しく見つかるかテスト
    """
    top = find_top_student(students_with_scores)  # トップ学生検索
    assert top.name == "学生B"  # 学生Bが最高得点
    assert top.get_average() == 92.5  # 平均点が92.5


def test_static_method_validate_age():
    """
    静的メソッドの年齢検証が正しく動作するかテスト
    """
    assert Student.validate_age(20) is True  # 有効な年齢
    assert Student.validate_age(0) is False  # 無効(0歳)
    assert Student.validate_age(150) is False  # 無効(150歳)
    assert Student.validate_age(-5) is False  # 無効(負数)


# --- パラメータ化テスト(複数のデータでテスト) ---
@pytest.mark.parametrize("score, expected", [
    (80, True),   # 80点は0-100の範囲内
    (100, True),  # 100点は0-100の範囲内
    (0, True),    # 0点は0-100の範囲内
    (101, False), # 101点は範囲外
    (-1, False),  # -1点は範囲外
])
def test_score_validation_parametrized(sample_student, score, expected):
    """
    様々な点数で検証をテスト
    
    Args:
        sample_student: フィクスチャ
        score: テストする点数
        expected: 期待される結果(True=有効, False=無効)
    """
    if expected:  # 有効な場合
        sample_student.add_score(score)  # エラーなく追加される
        assert score in sample_student.scores  # スコアリストに含まれる
    else:  # 無効な場合
        with pytest.raises(ValueError):  # ValueErrorが発生
            sample_student.add_score(score)


# ============================================
# --- unittest用テストコード ---
# ファイル名: test_student_unittest.py

import unittest  # unittestフレームワークをインポート
from python_basics_tutorial import Student, calculate_class_average, find_top_student


class TestStudent(unittest.TestCase):
    """
    Studentクラスをテストするテストケースクラス
    unittest.TestCaseを継承する
    """
    
    def setUp(self):
        """
        各テストメソッドの前に実行される初期化処理
        """
        self.student = Student("テスト太郎", 20, 2)  # テスト用学生を作成
    
    def tearDown(self):
        """
        各テストメソッドの後に実行されるクリーンアップ処理
        """
        # 必要に応じてリソースの解放などを行う
        pass
    
    def test_student_creation(self):
        """
        学生インスタンスが正しく作成されるかテスト
        """
        self.assertEqual(self.student.name, "テスト太郎")  # 等しいか検証
        self.assertEqual(self.student.age, 20)  # 等しいか検証
        self.assertEqual(self.student.grade, 2)  # 等しいか検証
        self.assertEqual(self.student.scores, [])  # 等しいか検証
    
    def test_add_score_valid(self):
        """
        有効な点数が正しく追加されるかテスト
        """
        self.student.add_score(85)  # 点数追加
        self.assertEqual(len(self.student.scores), 1)  # 長さが1
        self.assertIn(85, self.student.scores)  # 85が含まれる
    
    def test_add_score_invalid(self):
        """
        無効な点数でエラーが発生するかテスト
        """
        with self.assertRaises(ValueError):  # ValueErrorが発生することを検証
            self.student.add_score(150)  # 無効な点数
        
        with self.assertRaises(ValueError):  # ValueErrorが発生することを検証
            self.student.add_score(-10)  # 無効な点数
    
    def test_get_average_no_scores(self):
        """
        スコアなしでNoneが返されるかテスト
        """
        self.assertIsNone(self.student.get_average())  # Noneであることを検証
    
    def test_get_average_with_scores(self):
        """
        スコアありで正しい平均が返されるかテスト
        """
        self.student.add_score(80)  # 点数追加
        self.student.add_score(90)  # 点数追加
        self.student.add_score(70)  # 点数追加
        
        self.assertEqual(self.student.get_average(), 80.0)  # 平均が80.0
    
    def test_is_passing(self):
        """
        合格判定が正しく動作するかテスト
        """
        self.student.add_score(70)  # 点数追加
        self.student.add_score(80)  # 点数追加
        
        self.assertTrue(self.student.is_passing())  # Trueであることを検証
        self.assertFalse(self.student.is_passing(80))  # Falseであることを検証
    
    def test_static_method(self):
        """
        静的メソッドのテスト
        """
        self.assertTrue(Student.validate_age(20))  # Trueであることを検証
        self.assertFalse(Student.validate_age(0))  # Falseであることを検証
        self.assertFalse(Student.validate_age(150))  # Falseであることを検証


class TestFunctions(unittest.TestCase):
    """
    モジュールレベルの関数をテストするクラス
    """
    
    def setUp(self):
        """
        テスト用の学生データを準備
        """
        self.student1 = Student("学生A", 20, 2)  # 学生A作成
        self.student1.add_score(80)  # 点数追加
        self.student1.add_score(90)  # 点数追加
        
        self.student2 = Student("学生B", 19, 1)  # 学生B作成
        self.student2.add_score(85)  # 点数追加
        self.student2.add_score(95)  # 点数追加
        
        self.students = [self.student1, self.student2]  # 学生リスト
    
    def test_calculate_class_average(self):
        """
        クラス平均計算のテスト
        """
        class_avg = calculate_class_average(self.students)  # クラス平均計算
        self.assertEqual(class_avg, 87.5)  # 平均が87.5
    
    def test_calculate_class_average_empty(self):
        """
        空リストでNoneが返されるかテスト
        """
        self.assertIsNone(calculate_class_average([]))  # Noneであることを検証
    
    def test_find_top_student(self):
        """
        トップ学生検索のテスト
        """
        top = find_top_student(self.students)  # トップ学生検索
        self.assertEqual(top.name, "学生B")  # 学生Bがトップ
        self.assertEqual(top.get_average(), 90.0)  # 平均90.0


# --- unittestをスクリプトとして実行する場合 ---
if __name__ == '__main__':
    unittest.main()  # すべてのテストを実行