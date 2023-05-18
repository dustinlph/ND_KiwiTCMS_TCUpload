# KiwiTCMS_TCUpload

## Step
1. 先執行 pre_work.py 確認是不是有必要檔案
2. 如果沒有會需要建立一個 .tcms.conf 檔案
3. 其中需要填入的資料
   1. url: kiwi TCMS URL
   2. username
   3. password
## 上傳 Testcase
1. 使用 excel 開立測項
2. 格式須符合 template 中 demo 格式，且需要確認在 Kiwi TCMS 系統中所定義的 Product, Category 是否都已建立
3. excel 編輯完之後，下載並儲存為 .csv 格式，並將檔案存放在 template 資料夾中
4. 透過執行腳本批次將測項開到 Kiwi TCMS 系統上 `python create_tc.py "demo.csv"`