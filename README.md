# flexible-template-matching

Point(x,y) là điểm.  
Line(p1, p2) là đường thẳng đi qua điểm p1, p2.  
Region(top, left, right, bottom) là một vùng hình tứ giác tạo bởi 4 điểm top, left, right, bottom.  
Template(image, region) là template được xác định từ ảnh và vùng tìm kiếm.   
FlexTM() là khởi tạo cái dùng để template matching.  
FlexTM.findTemplateMax(template, image, searchRegion) là tìm vị trí template trên ảnh trong vùng tìm kiếm bằng templatematching.  
Cụ thể vào test.py mà xem nhé  

Lưu ý: Chỉ dùng với ảnh trắng đen :>  
