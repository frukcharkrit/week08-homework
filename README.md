# week08-homework
สำหรับส่งการบ้าน week08 วิชา dstoolbox
    (แก้ไขหน้า 29.html)
    ## แก้ไขที่บรรทัดที่ 709 (<div :class="{ 'active': currentSlide === 20 }" class="slide gradient-bg flex-col justify-center items-center text-white">) 
    - แก้ไขให้เป็น currentSlide === 28 เนื่องจากมีการเขียนหน้าซ้ำทำให้ตัวโปรแกรมหาเลข 28 (ถัดจาก 27) ไม่เจอจาก script ( nextSlide() {this.currentSlide = (this.currentSlide + 1) % this.totalSlides;},) จึงไม่มีอะไรแสดงผลออกมา

## ผลลัพธ์การรัน pycaretflow.py
 Model  Accuracy     AUC  Recall   Prec.  \
lr                    Logistic Regression    0.7689  0.8047  0.5602  0.7208
ridge                    Ridge Classifier    0.7670  0.8060  0.5497  0.7235
lda          Linear Discriminant Analysis    0.7670  0.8055  0.5550  0.7202
rf               Random Forest Classifier    0.7485  0.7911  0.5284  0.6811
nb                            Naive Bayes    0.7427  0.7955  0.5702  0.6543
catboost              CatBoost Classifier    0.7410  0.7993  0.5278  0.6630
gbc          Gradient Boosting Classifier    0.7373  0.7914  0.5550  0.6445
ada                  Ada Boost Classifier    0.7372  0.7799  0.5275  0.6585
et                 Extra Trees Classifier    0.7299  0.7788  0.4965  0.6516
qda       Quadratic Discriminant Analysis    0.7282  0.7894  0.5281  0.6558
lightgbm  Light Gradient Boosting Machine    0.7133  0.7645  0.5398  0.6036
knn                K Neighbors Classifier    0.7001  0.7164  0.5020  0.5982
dt               Decision Tree Classifier    0.6928  0.6512  0.5137  0.5636
xgboost         Extreme Gradient Boosting    0.6928  0.7571  0.5070  0.5779
dummy                    Dummy Classifier    0.6518  0.5000  0.0000  0.0000
svm                   SVM - Linear Kernel    0.5954  0.5914  0.3395  0.4090

              F1   Kappa     MCC  TT (Sec)
lr        0.6279  0.4641  0.4736     0.573
ridge     0.6221  0.4581  0.4690     0.008
lda       0.6243  0.4594  0.4695     0.007
rf        0.5924  0.4150  0.4238     0.033
nb        0.6043  0.4156  0.4215     0.008
catboost  0.5851  0.4005  0.4078     0.622
gbc       0.5931  0.4013  0.4059     0.026
ada       0.5796  0.3926  0.4017     0.019
et        0.5596  0.3706  0.3802     0.034
qda       0.5736  0.3785  0.3910     0.007
lightgbm  0.5650  0.3534  0.3580     0.197
knn       0.5413  0.3209  0.3271     0.367
dt        0.5328  0.3070  0.3098     0.007
xgboost   0.5335  0.3068  0.3131     0.879
dummy     0.0000  0.0000  0.0000     0.009
svm       0.2671  0.0720  0.0912     0.008

In [7]: print(best)
LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                   intercept_scaling=1, l1_ratio=None, max_iter=1000,
                   multi_class='auto', n_jobs=None, penalty='l2',
                   random_state=123, solver='lbfgs', tol=0.0001, verbose=0,
                   warm_start=False)


1. โมเดลชนะเลิศ: Logistic Regression (lr)
โมเดล Logistic Regression ทำผลงานได้ดีที่สุดในภาพรวม โดยมีค่าเฉลี่ยจากการ Cross-validation ดังนี้:

Accuracy (ความแม่นยำรวม): 76.89% หมายความว่าทายถูกประมาณ 77 จาก 100 เคส

AUC (พื้นที่ใต้กราฟ ROC): 0.8047 ค่านี้บ่งบอกว่าโมเดลมีความสามารถในการแยกแยะระหว่างคนที่เป็นเบาหวานกับไม่เป็นได้ค่อนข้างดี (เข้าใกล้ 1 ยิ่งดี)

2. ข้อสังเกตสำคัญ: Linear vs. Tree-based Models
สิ่งที่น่าสนใจมากในตารางนี้คือ 3 อันดับแรกเป็น Linear Models ทั้งหมด ได้แก่:

Logistic Regression (lr)

Ridge Classifier (ridge)

Linear Discriminant Analysis (lda)

ในขณะที่โมเดลตระกูล Tree ที่ซับซ้อนกว่าอย่าง Random Forest (rf) หรือ XGBoost (xgboost) กลับได้คะแนนน้อยกว่า

วิเคราะห์: ข้อมูลชุดนี้ (Pima Indians Diabetes) น่าจะมีความสัมพันธ์ของตัวแปรในลักษณะเชิงเส้น (Linear) ค่อนข้างมาก หรือข้อมูลอาจจะมีขนาดเล็กและมี Noise ทำให้โมเดลที่ซับซ้อนเกินไป (Complex models) เกิดการ Overfit หรือเรียนรู้ได้ยากกว่าโมเดลพื้นฐาน

3. จุดที่น่ากังวล: ค่า Recall (ความไว) ต่ำเกินไป
นี่คือจุดที่สำคัญที่สุดสำหรับการวิเคราะห์โจทย์ทางการแพทย์:

Recall ของ lr อยู่ที่ 0.5602 (หรือ 56%)

ความหมาย: ในบรรดาคนที่เป็นเบาหวานจริงๆ 100 คน โมเดลนี้ตรวจเจอเพียง 56 คน อีก 44 คนถูกทำนายว่าปกติ (False Negative)

ผลกระทบ: ในทางการแพทย์ การปล่อยให้คนป่วยหลุดรอดไป (ทำนายว่าไม่ป่วย) อันตรายกว่าการทำนายผิดว่าป่วย (False Positive) ดังนั้นค่า Recall 56% ถือว่า ยังไม่ดีพอสำหรับการใช้งานจริง

4. การวิเคราะห์พารามิเตอร์ของ best model
คำสั่ง print(best) แสดงให้เห็นว่า PyCaret ใช้ค่า Default ของ Scikit-learn สำหรับ Logistic Regression:

C=1.0: ค่า Regularization ระดับกลาง

class_weight=None: นี่คือสาเหตุหนึ่งที่ Recall ต่ำ เพราะข้อมูลชุดนี้คนไม่เป็นเบาหวาน (0) เยอะกว่าคนเป็นเบาหวาน (1) เมื่อไม่ปรับน้ำหนัก โมเดลจึงเอนเอียงไปทายผลกลุ่มส่วนใหญ่ (Majority Class)

solver='lbfgs': อัลกอริทึมมาตรฐานสำหรับการหาคำตอบ
