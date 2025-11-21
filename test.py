# from loguru import logger

# logger.add("app.log", level="WARNING")

# logger.debug("これは出力されません")
# logger.info("これは出力されます")
# logger.warning("これは出力されません（INFOのみなら）")


# from loguru import logger

# def info_only(record):
#     return record["level"].name == "INFO"

# logger.add("info_only.log", filter=info_only)

# logger.debug("DEBUG → 出ない")
# logger.info("INFO → 出る")
# logger.warning("WARNING → 出ない")
# logger.error("ERROR → 出ない")

# from loguru import logger

# # デフォルト（INFO 以上がコンソールへ）を消す
# logger.remove()

# # INFO のみ通すコンソール出力を追加
# logger.add(
#     sink=lambda msg: print(msg, end=""),
#     filter=lambda r: r["level"].name == "INFO"
# )

# logger.debug("DEBUG → 出ない")
# logger.info("INFO → 出る（コンソール）")
# logger.warning("WARNING → 出ない")
# logger.error("ERROR → 出ない")




# from loguru import logger

# logger.info("Hello, Loguru!")

# # すべてのレベルでログを出力
# logger.trace("これは TRACE レベルです")
# logger.debug("これは DEBUG レベルです")
# logger.info("これは INFO レベルです")
# logger.success("これは SUCCESS レベルです")
# logger.warning("これは WARNING レベルです")
# logger.error("これは ERROR レベルです")
# logger.critical("これは CRITICAL レベルです")

# from loguru import logger

# def process_order(order_id, amount):
#     # TRACE: 関数の入り口や詳細情報を確認したいとき
#     logger.trace(f"process_order() 呼び出し: order_id={order_id}, amount={amount}")

#     # DEBUG: 処理の分岐や中間結果を確認したいとき
#     if amount <= 0:
#         logger.debug(f"注文額が0以下: order_id={order_id}, amount={amount}")
#         return False

#     # INFO: ユーザーや開発者が普通に知っておきたい進捗情報
#     logger.info(f"注文を処理中: order_id={order_id}, amount={amount}")

#     # SUCCESS: 特に重要ではないが、うまく処理できたことを明示
#     logger.success(f"注文処理完了: order_id={order_id}")

#     # WARNING: ちょっと気になる状態や注意喚起
#     if amount > 10000:
#         logger.warning(f"大口注文: order_id={order_id}, amount={amount}")

#     # ERROR: 明らかに処理できなかったエラー
#     if order_id is None:
#         logger.error("order_id が None です")
#         return False

#     # CRITICAL: すぐに対応が必要な重大障害
#     # 例: 支払いシステムが落ちている
#     payment_system_ok = True
#     if not payment_system_ok:
#         logger.critical("支払いシステムが利用不可！即対応必要！")
#         return False

#     return True

# # 実行例
# process_order(1, 500)
# process_order(2, 15000)
# process_order(None, 100)







# from loguru import logger

# def vending_machine(action, amount=None):
#     # TRACE: ボタンが押された瞬間や細かい内部状態の記録
#     logger.trace(f"アクション開始: {action}, 金額: {amount}")

#     # DEBUG: 処理の分岐や計算中の細かい情報
#     if action == "insert_coin":
#         logger.debug(f"硬貨が投入された: {amount}円")
#     elif action == "select_item":
#         logger.debug("商品が選択された")
#     elif action == "dispense":
#         logger.debug("商品を出す処理開始")
#     else:
#         logger.debug(f"未知の操作: {action}")

#     # INFO: ユーザーに見える基本的な進捗
#     if action == "insert_coin":
#         logger.info(f"{amount}円が投入されました")
#     elif action == "select_item":
#         logger.info("商品が選択されました")
#     elif action == "dispense":
#         logger.info("商品をお渡しします")

#     # SUCCESS: 商品が正常に出たときの成功ログ
#     if action == "dispense":
#         logger.success("商品が正常に出されました")

#     # WARNING: おつりが少ない、在庫が少ないなど注意が必要な状況
#     if action == "select_item" and amount and amount < 100:
#         logger.warning("投入金額が不足している可能性があります")

#     # ERROR: 投入金額が足りない場合など、エラー状態
#     if action == "dispense" and (amount is None or amount < 100):
#         logger.error("商品を出すには金額が不足しています")

#     # CRITICAL: 自動販売機のシステムが停止したなどの重大障害
#     system_ok = True  # ここは例です
#     if not system_ok:
#         logger.critical("システム障害！即対応必要！")

# # 動作例
# vending_machine("insert_coin", 100)
# vending_machine("select_item")
# vending_machine("dispense", 100)
# vending_machine("dispense", 50)  # エラーの例


# from loguru import logger

# # ログをファイルに出力（デフォルトで追記モード）
# logger.add("logfile.log", level="DEBUG")  # DEBUG 以上のログを保存

# logger.debug("これは DEBUG レベルのログです")
# logger.info("これは INFO レベルのログです")
# logger.warning("これは WARNING レベルのログです")
# logger.error("これは ERROR レベルのログです")
# logger.critical("これは CRITICAL レベルのログです")



from loguru import logger

# # デフォルトのコンソール出力を削除
# logger.remove()  

# # 1. ファイルに全レベルのログを保存
# logger.add("logfile.log", level="DEBUG", encoding="utf-8")  # DEBUG以上をファイルに保存

# # 2. コンソールには INFO レベルのみ表示
# logger.add(lambda msg: print(msg, end=""), level="INFO", filter=lambda record: record["level"].name == "INFO")

# # ログテスト
# logger.debug("DEBUG レベル（ファイルのみ）")
# logger.info("INFO レベル（コンソールにも表示）")
# logger.success("SUCCESS レベル（ファイルのみ）")
# logger.warning("WARNING レベル（ファイルのみ）")
# logger.error("ERROR レベル（ファイルのみ）")
# logger.critical("CRITICAL レベル（ファイルのみ）")


# logger.remove()

# logger.add(
#     "logfile.log",
#     filter=lambda r: r["level"].name in ("DEBUG", "INFO")
# )

# logger.debug("DEBUG → 出る")
# logger.info("INFO → 出る")
# logger.warning("WARNING → 出ない")
# # logger.error("ERROR → 出ない")


# from loguru import logger

# # デフォルトコンソール出力を削除
# logger.remove()  

# # コンソールに DEBUG と WARNING のみ表示
# logger.add(
#     lambda msg: print(msg, end=""),
#     level="DEBUG",  # 最低レベルを DEBUG に設定
#     filter=lambda record: record["level"].name in ["DEBUG", "WARNING"]
# )

# # ファイルには全レベルのログを保存
# logger.add("logfile.log", level="DEBUG", encoding="utf-8")

# # ログテスト
# logger.debug("DEBUG（コンソールとファイル）")
# logger.info("INFO（ファイルのみ）")
# logger.success("SUCCESS（ファイルのみ）")
# logger.warning("WARNING（コンソールとファイル）")
# logger.error("ERROR（ファイルのみ）")
# logger.critical("CRITICAL（ファイルのみ）")

# from loguru import logger

# # デフォルトのコンソール出力を削除
# logger.remove()

# # コンソールに INFO レベルだけ表示
# logger.add(lambda msg: print(msg, end=""),
#            filter=lambda record: record["level"].name == "INFO")

# # ログテスト
# logger.debug("DEBUG（表示されない）")
# logger.info("INFO（コンソールに表示される）")
# logger.warning("WARNING（表示されない）")


# from loguru import logger

# # デフォルトコンソール出力を削除
# logger.remove()

# # コンソールに DEBUG と WARNING だけ表示
# logger.add(
#     lambda msg: print(msg, end=""),  # 標準出力に出す
#     level="DEBUG",                   # 最低レベルは DEBUG
#     filter=lambda record: record["level"].name in ["DEBUG", "WARNING"]
# )

# # ログテスト
# logger.debug("DEBUG（コンソールに表示）")
# logger.info("INFO（表示されない）")
# logger.success("SUCCESS（表示されない）")
# logger.warning("WARNING（コンソールに表示）")
# logger.error("ERROR（表示されない）")
# logger.critical("CRITICAL（表示されない）")

# from loguru import logger

# # デフォルトコンソール出力を削除
# logger.remove()

# # DEBUG だけを debug.log に保存
# logger.add(
#     "debug.log",
#     filter=lambda record: record["level"].name == "DEBUG",
#     encoding="utf-8"
# )

# # ログテスト
# logger.debug("DEBUG（debug.log のみ）")
# logger.info("INFO（どのファイルにも保存されない）")
# logger.success("SUCCESS（どのファイルにも保存されない）")
# logger.warning("WARNING（warning.log のみ）")
# logger.error("ERROR（error.log のみ）")
# logger.critical("CRITICAL（どのファイルにも保存されない）")

# from loguru import logger

# # デフォルトコンソール出力を削除
# logger.remove()

# # DEBUG と WARNING を logs.txt に保存
# logger.add(
#     "logfile.log",
#     filter=lambda record: record["level"].name in ["DEBUG", "WARNING"],
#     encoding="utf-8"
# )

# # ログテスト
# logger.debug("DEBUG（logs.txt に保存）")
# logger.info("INFO（保存されない）")
# logger.success("SUCCESS（保存されない）")
# logger.warning("WARNING（logs.txt に保存）")
# logger.error("ERROR（保存されない）")
# logger.critical("CRITICAL（保存されない）")


# from loguru import logger

# # デフォルトのコンソール出力を削除
# logger.remove()  

# # 1. ファイルに全レベルのログを保存
# logger.add("logfile.log", level="DEBUG", encoding="utf-8")  # DEBUG以上をファイルに保存

# # 2. コンソールには INFO レベルのみ表示
# logger.add(lambda msg: print(msg, end=""), level="INFO", filter=lambda record: record["level"].name == "INFO")

# # ログテスト
# logger.debug("DEBUG レベル（ファイルのみ）")
# logger.info("INFO レベル（コンソールにも表示）")
# logger.success("SUCCESS レベル（ファイルのみ）")
# logger.warning("WARNING レベル（ファイルのみ）")
# logger.error("ERROR レベル（ファイルのみ）")
# logger.critical("CRITICAL レベル（ファイルのみ）")


from loguru import logger

class Main():
    def __init__(self):
        logger.remove()
        # INFO のみ通すコンソール出力を追加
        logger.add(
            sink=lambda msg: print(msg, end=""),
            filter=lambda r: r["level"].name in ("DEBUG", "INFO"),
            colorize=True
        )

        # mainでデバッグを使う
        logger.debug("mainの初期化完了しました。")

        # Sample_1クラスの呼び出し
        self.sample_1 = Sample_1(self)
        
        # Sample_2クラスの呼び出し
        self.sample_2 = Sample_2(self)


class Sample_1():
    def __init__(self, parent):
        self.parent = parent
        print("これはプリント文です")
        self.debug_test()

    def debug_test(self):
        info_1 = "info"
        # info文
        logger.info(f"インフォ: Sample_1クラス: 関数内の出力{info_1}")

class Sample_2():
    def __init__(self, parent):
        self.parent = parent
        debug_1 = "debug"
        # debug文
        logger.debug(f"デバッグ: Sample_2クラス: __init__文内の出力{debug_1}")

if __name__ == "__main__":
    Main()
