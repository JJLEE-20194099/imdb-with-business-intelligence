# Phân tích nghiệp vụ thông minh

***Chú ý:*** Do có viết 1 số công thức nên nhóm tôi khuyên bạn nên dùng file sau để xem đầy đủ chính xác và chi tiết hơn:
https://hackmd.io/1GFmNyJIT4C4ecAF6Czgcw?view


- [Phân tích nghiệp vụ thông minh](#)
  * [Người đóng góp](#)
  * [Phân công công việc](#)
- [Giới thiệu đề tài](#)
- [Thu thập dữ liệu](#)
- [Tích hợp dữ liệu](#)
- [Làm sạch và tiền xử lý dữ liệu](#)
- [IMDB datasets](#)
- [Khám phá dữ liệu](#)
- [Một số khái niệm và độ đo cần thiết cho bài toán](#)
- [Mô hình](#)
 
     

      
- [Hướng dẫn chạy chương trình](#)
  * [Thu thập dữ liệu](#)
  * [Làm sạch và tiền xử lý dữ liệu](#)
  * [Khám phá dữ liệu](#)
  * [Thử nghiệm các mô hình](#)
- [Demo](#)

## 1. Tự đánh giá dựa trên phân tích nghiệp vụ thông minh project

|Nội dung||
|-|-|
|Thu thập dữ liệu bằng cách sử dụng thư viện BeautifulSoup| Hoàn thành |
| Tích hợp dữ liệu| Hoàn Thành|
| Làm sạch và tiền xử lý dữ liệu| Hoàn thành|
| Phân tích và khám phá dữ liệu các bộ film |Hoàn Thành|
|Dự đoán điểm rating đánh giá cho bộ phim||

**Kết quả:** Nhóm đã có những góc nhìn 1 cách tổng quan về các phương pháp dự đoán rating, từ đó phần nào biết được bộ phim có thành công hay không


## 2.Người đóng góp

|Họ & tên|MSSV|
|-|-|
|Lê Thành Long| 20194099
|Ninh Văn Nghĩa| 20190060
|Đào Nguyễn Tiến Huy| 20194077
|Nguyễn Thị Thùy Trang| 20194190



***This is a project about how our group predict success of a movie based on some information***

***My system's name is IMDB_WITH_BI***

***@Author: LTHT GROUP***

---

## 3. Phân công công việc trong nhóm

|Họ & tên|Nội dung công việc|
|-|-|
|Lê Thành Long| Code phần crawl data từ trang https://www.imdb.com/ và xây dựng mạng dự đoán rating cho một bộ phim
|Cả nhóm| Trực quan hóa dữ liệu, và đóng góp ý kiến hoàn chỉnh code, báo cáo và slide.

## 4. Giới thiệu đề tài:

Một trong những điều quan trọng mà bất cứ những công ty sản xuất phim quan tâm đó chính là bộ phim này có thực sự thành công hay không. Bộ phim này được người dùng đánh giá cao hay không. Nhóm chúng tôi tập trung vào các bài toán dự đoán rating của bộ phim.


Các mô hình nhóm sử dụng đó chính là: Mô hình ***random forest***, ***regression***, ... Trong đó nhóm có đề xuất một giải thuật có tên là ***MIBPS - Multi Information-Based Prediction System***

## 5. Thu thập dữ liệu

Nhóm chúng tôi đã thu thập dữ liệu từ trang review phim nổi tiếng https://www.imdb.com/ mặc dù trên mạng đã có rất nhiều bộ data về cái này tuy nhiên bộ datasets của nhóm chúng tôi rất dồi dào về các thông tin chi tiết phim và thông tin rating và đặc biệt các bộ phim trên bộ dataset của nhóm chúng tôi toàn là phim mới đồng nghĩa là các review ở các bộ phim này cũng là gần đây.

***Thư viện để thu thập dữ liệu là BeautifulSoup***
(Code thu thập dữ liệu ở trong mục src của project)

Chúng tôi có những hàm số cơ bản khi ***crawl dữ liệu như sau:***


+ get_content(url): Lấy ra nội dung html của trang
+ generate_imdb_genre_links_from_base_genre_url(url, pagination_idx): Lấy ra nhiều trang 
+ get_all_film_links_from_a_imdb_genre_url(url): Lấy ra tất cả url bộ phim trong 1 trang


***Chú ý***: Nhiều hàm khác bạn đọc tham khảo trong ***src/url_functions.py*** của project


## 6. Tích hợp dữ liệu

Khi crawl về thì sẽ có khoảng 14 thể loại phim chính trong đó có các id của từng loại

Tích hợp các file id lại với nhau và tiếp tục thu thập dữ liệu về phim và rating

## 7. Làm sạch và tiền xử lý dữ liệu

Quá trình thu thập không tránh khỏi sai sót và lỗi đặc biệt trong quá trình thu thập data thì imdb có cơ chế chống crawl hàng loạt nên bộ dataset có 1 số missing value nhất định:

***Một số bước cơ bản của làm sạch và tiền xử lý dữ liệu:***

+ Đối với các bộ phim có title bằng nan thì xóa luôn
+ 1 bộ phim có thể thuộc nhiều thể loại (trong bộ data có 27 thể loại), tạo thêm 27 cột có tên 27 thể loại, điền vào giá trị 1 nếu bộ phim thuộc thể loại đó, còn điền giá trị 0 nếu ngược lại
+ Bỏ đi các bộ phim, user, rating trùng lặp nhau
+ Label encoder cho những trường dữ liệu categorical
+ + ....


Ta sẽ tách bộ dữ liệu thành hai phần:
+ Phần thứ nhất: thông tin title, runtime, tóm tắt bộ phim, thế loại, ...
+ Phần thứ hai: ***rating total*** và ***average rating***. Đặc biệt để đảm bảo cho độ tin cậy ta chọn giá trị dự đoán là ***log(rating total x average rating)***.

Sở dĩ ta lấy logarit vì do ***phân phối của rating total x average rating khá nhọn và lệch***

+ Trước khi lấy logarit

![](https://i.imgur.com/fJamGNJ.png)


+ Sau khi lấy logarit

![](https://i.imgur.com/rrmVC16.png)


## 8. IMDB datasets


**Tổng quan và mô tả dữ liệu được sử dụng:**

- **movie/ml_detail.csv:**  8352 dòng và 45 cột

|    | Column             | Dtype   | Value range   | Description                                                                                                            |
|---:|:-------------------|:--------|:--------------|:-----------------------------------------------------------------------------------------------------------------------|
|  0 | movie id                 | string   | nan          | id của bộ film
|  1 | title               | string  | nan           | Tên của bộ phim                                                                                                       |
|  2 | series         | string |nan        | Có phải là series film hay không hay và film lẻ                                                                                         |
|  3 | release year          | int64   | >= 0          | Năm phát hành bô phim                                                             |
|  4 | certification             | string | nan          | Tagger cho bộ phim, phim được phụ huynh cho phép, phim người lớn, ...                                     |
|  5 | duration              | string | nan           | Thời lượng của bộ phim                                                                                                 |                                                  |
|  7 | average rating           | float   | >= 0          | số rating trung bình                                                                                     |
|  8 |rating total             | string   | nan          | tổng số lượt rating                                                                                      |
 9 | content             | string   | nan          | Content của bộ phim                                  |
| 10 | ...             | ...   | ...          | Bạn đọc tham khảo trong dataset                                                |


Chúng tôi chia tập dữ liệu thành 3 phần đó chính là

+ ***10% cho tập test***
+ ***10% cho tập valiation***
+ ***80% cho tập train***
            
## 9. Khám phá dữ liệu:

Nhóm chỉ nêu ra 1 số khám phá, chi tiết các bạn đọc ở trong project file ***[4] Data Exploration.ipynb***

***Điểm trung bình rating và số lượng người xem theo từng thể loại***
![](https://i.imgur.com/JaSf6m6.png)


***Phân bố người đánh giá theo từng ngày***
![](https://i.imgur.com/v2rqkZz.png)

***Phân bố điểm rating trung bình***
![](https://i.imgur.com/irS23h4.png)


***Rating trung bình và số lượng bộ phim ứng với từng khoảng doanh thu***
![](https://i.imgur.com/m2G5sL2.png)




## 10. Một số khái niệm và độ đo cần thiết trong project

### 10.1 SIA - Soft Interval Accuracy
Một dự đoán được gói là đúng nói chênh lệch giữa dự đoán và thực tế <= siêu tham số epsilon:
$|y_i - \hat{y_i}| <= eps$
Và ***SIA*** sẽ bằng số mẫu đúng trên toàn bộ mẫu

---

### 10.2 MAE - Mean Absolute Error

$MAE(y, \hat{y}) = \frac{1}{m} \sum\limits_{i = 1}^{m}|y_i - \hat{y_i}|$

---

### 10.3 MSE - Mean Squared Error

$MSE(y, \hat{y}) = \frac{1}{m} \sum\limits_{i = 1}^{m}(y_i - \hat{y_i})^2$

---

### 10.4 RMSE - Root Mean Squared Error

$RMSE(y, \hat{y}) = \sqrt{\frac{1}{m} \sum\limits_{i = 1}^{m}(y_i - \hat{y_i})^2}$

---


## 11. Mô hình

### 11.1 Những mô hình cơ bản

![](https://i.imgur.com/MVXltlc.png)

#### 11.1.1 Mô hình Regression

##### 11.1.1.1 Linear Regression

Mô hình đầu tiên nhóm chúng tôi muốn thử đó chính là mô hình ***linear regression***

***Hàm mất mát***

Hàm lỗi nhóm chúng tôi sử dụng là trung bình cộng của bình phương độ chênh lệch kết quả dự doán và kết quả thực tế.

$\text{RSS}(y, \hat{y}) = {\frac{1}{m} \sum\limits_{i=1}^{m} (y_i - \hat{y}_i)^2}$

$Loss(y, \hat{y}) = \text{RSS}(y, \hat{y})$

***Kết quả***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.45|1.82|0.4176|
|val|1.46|1.83|0.4236|
|test|1.44|1.80|0.4354|

##### 11.1.1.2 Ridge Regression

Do kết quả chưa thực sự tốt và mô hình đang gặp phải vấn đề ***overfitting*** trên độ đo ***SIA*** nên dùng thêm l2 regularization

Khi đó ta có công thức ***hàm mất mát*** như sau:

Hàm lỗi nhóm chúng tôi sử dụng là trung bình cộng của bình phương độ chênh lệch kết quả dự doán và kết quả thực tế.

$\text{RSS}(y, \hat{y}) = {\frac{1}{m} \sum\limits_{i=1}^{m} (y_i - \hat{y}_i)^2}$

$Loss(y, \hat{y}) = \text{RSS}(y, \hat{y}) + \text{Regularization_Func}$

Chúng tôi ***chọn khoảng giá trị*** để ***tuning siêu tham số alpha***

Khi đó ta có ***kết quả*** sau:

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.45|1.81|0.4176|
|val|1.46|1.83|0.4236|
|test|1.43|1.80|0.4354|

***Nhận xét:*** Mặc dù đã chọn ra siểu tham số $\alpha$ tốt nhất để tránh trường hợp overfitting. Tuy nhiên kết quả không khác nhau là mấy.

Chúng tôi có thể khẳng định mô hình ***regression*** không phù hợp với tập dữ liệu này. Chúng tôi đến với mô hình tiếp theo

#### 11.1.2 Mô hình Random Forest

Ở mục này chúng tôi sẽ chứng minh sự ảnh hưởng của ***nội dung và tiểu đề bộ phim*** đến kết quả dự đoán được

##### 11.1.2.1 Khi không dùng nội dung tóm tắt của bộ phim

***Tuning số lượng cây***

+ Khi ***n_estimators = 50***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.3362|1.7048|0.4653|
|val|1.3937|1.7631|0.4461|
|test|1.3880|1.7629|0.4383|

+ Khi ***n_estimators = 100***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.3357|1.7044|0.4658|
|val|1.3934|1.7624|0.4442|
|test|1.3860|1.7616|0.4402|

+ Khi ***n_estimators = 200***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.3358|1.7043|0.4652|
|val|1.3935|1.7632|0.4473|
|test|1.3867|1.7618|0.4402|

+ Khi ***n_estimators = 500***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|1.3357|1.7042|0.4652|
|val|1.3935|1.7629|0.4473|
|test|1.3857|1.7606|0.4402|

***Dựa vào bảng kết quả trên chúng tôi chọn tham số n_estimators=200***

***Nhận xét***: Kết quả tốt hơn mô hình ***regression***. Ta sẽ tiếp tục cải thiện mô hình này bằng cách thêm các yếu tố ***nội dung và tiêu đề bộ phim*** vào.

##### 11.1.2.2 Khi dùng nội dung tóm tắt của bộ phim

Chọn ***n_estimators = 200***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|0.4587|0.6014|0.8974|
|val|1.2403|1.6159|0.50964|
|test|1.2469|1.6328|0.50961|

***Nhận xét***: Khi thêm yếu tố ***nội dung***  vào các mô hình thì kết quả tốt hơn rất nhiều. Điều này nói lên ***yếu tố tiêu đề và nội dung tóm tắt*** ảnh hưởng một phần đến việc đánh giá đúng bộ phim của người dùng


#### 11.1.3 Mô hình Deep Learning cơ bản

Mặc dù mô hình ***Random Forest*** đã tốt hơn so với các phương pháp khác tuy nhiên chúng ta không thể không kiểm tra bài toán với các mô hình mạng ***Nơ ron nhân tạo***. Dữ liệu có ***nhiều chiều và phực tạp*** là một lý do sử dụng mạng ***neural network***. Mạng ***nơ ron nhân tạo*** có thể mô hình hóa tốt và tạo ra một hàm ***phi tuyến*** để xấp xỉ với trường dữ liệu.

Chúng tôi thử với mô hình ***mạng nơ ron nhân tạo tuyến tính cơ bản*** sau:
![](https://i.imgur.com/FdIyz4B.png)

***Mô hình***
![](https://i.imgur.com/kkfbmXq.png)



***Kết quả***

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|0.4142|0.5401|0.9231|
|val|1.1163|1.3752|0.6127|
|test|1.1437|1.5921|0.6254|


***Nhận xét***: Đúng như suy nghĩ ban đầu mạng ***neural*** có vẻ đã học tốt được nhiều thuộc tính quan trọng và mô hình hóa gần với dữ liệu hơn. Tuy nhiên do nhóm chúng tôi thấy mô hình vẫn chưa đủ tốt. Chúng tôi sẽ cải thiện kết quả trên bằng cách ***đề xuất một mô hình mới***



### 11. 2 Đề xuất giải thuật MIBPS - Multi Information Based Prediction System


![](https://i.imgur.com/QsWDLME.png)


Như chúng ta đã biết ***nội dung tóm tắt và tên*** của một bộ phim là một trong những yêu tố ảnh hưởng lớn đến việc người dùng vào xem bộ phim đó và sẽ ảnh hưởng phần nào đến việc người dùng hiểu và đánh giá bộ phim đó đúng hơn. Do đó tác động đến tổng điểm rating của người dùng đến bộ phim. Khi đó ta cũng có đánh giá khách quan hơn về sự thành công của một bộ phim

Áp dụng các kỹ thuật tiền xử lý và làm sạch dữ liệu trong xử lý ngôn ngữ tự nhiên như:

+ Loại bỏ stop word
+ Chỉnh chính tả cho từ
+ Chuyển các chữ viết tắt thành các cụm không viết tắt, ...

Đặc biệt chúng tôi dùnhg thêm một lớp Embedding mục đích để học được nhiều ngữ nghĩa hơn của một từ. Củ thể chúng tôi chọn ***laten-dim là 64***, nghĩa là chúng tôi vector hóa ngữ nghĩa của 1 từ bằng ***64 chiều khác nhau***.

Hơn thế nữa, trước khi concat các trường dữ liệu lại với nhau thì chúng tôi ***flatten embedding*** và cho qua một số lớp ***Dense***.

Vì sao lại như vậy?

Chúng tôi muốn học được những từ cần thiết đặc trưng và quan trọng nhất trong ***storyline và title***. Loại bỏ đi những đặc trưng không thực sự cần thiết

![](https://i.imgur.com/ASbgeZ7.png)


***Kết quả đạt được***:

|Dataset|MAE|RMSE|SIA 1|
|-|-|-|-|
|train|0.2384|0.4614|0.9532|
|val|1.0193|1.1532|0.8531|
|test|0.8956|0.9845|0.8921|

***Nhận xét***: Kết quả thực sự tốt hơn hẳn các mô hình trên. Sở dĩ có điều này vì mô hình học được ***đa thông tin*** từ bộ phim. Tuy nhiên thông tin chúng tôi học không phải là thông tin raw mà là thông tin đã được tiền xử lý và được trích xuất ra những đặc trưng quan trong nhất