import uuid

# hàm này dùng để tạo ngẫu nhiên 1 chuỗi: để cho slug của user khỏi bị trùng
def get_random_code():
    return (str(uuid.uuid4().hex[:10].replace('-', '').lower()))
