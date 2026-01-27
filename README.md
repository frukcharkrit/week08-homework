# week08-homework
สำหรับส่งการบ้าน week08 วิชา dstoolbox
    ## แก้ไขที่บรรทัดที่ 709 (<div :class="{ 'active': currentSlide === 20 }" class="slide gradient-bg flex-col justify-center items-center text-white">) 
    - แก้ไขให้เป็น currentSlide === 28 เนื่องจากมีการเขียนหน้าซ้ำทำให้ตัวโปรแกรมหาเลข 28 (ถัดจาก 27) ไม่เจอจาก script ( nextSlide() {this.currentSlide = (this.currentSlide + 1) % this.totalSlides;},) จึงไม่มีอะไรแสดงผลออกมา
