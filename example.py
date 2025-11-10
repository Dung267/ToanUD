import numpy as np
import csv

# Đặt tên file của bạn vào đây
FILE_PATH = 'Vidu\\monan.csv' 

# --- 1. ĐỌC VÀ XỬ LÝ DỮ LIỆU TỪ FILE CSV ---
try:
    with open(FILE_PATH, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # Bỏ qua hàng tiêu đề (header)
        header = next(reader)
        # Đọc chuỗi các món ăn
        sequence = [row[1] for row in reader] # Giả định món ăn ở cột thứ 2 (index 1)
except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file tại đường dẫn {FILE_PATH}. Vui lòng kiểm tra lại tên file và đường dẫn.")
    exit()
except Exception as e:
    print(f"Lỗi khi đọc file CSV: {e}")
    exit()

# Lấy trạng thái (món ăn) cuối cùng làm trạng thái ban đầu
initial_state_name = sequence[-1]
print(f"✅ Dữ liệu lịch sử đã đọc. Món ăn lần gần nhất (Hôm qua): **{initial_state_name}**\n")

# Lấy tất cả các trạng thái (món ăn) duy nhất
states = sorted(list(set(sequence)))
state_to_index = {state: i for i, state in enumerate(states)}
num_states = len(states)

# --- 2. TÍNH MA TRẬN ĐẾM (COUNT MATRIX) ---

# Khởi tạo ma trận đếm với kích thước NxN
count_matrix = np.zeros((num_states, num_states), dtype=int)

# Duyệt qua chuỗi để đếm các lần chuyển đổi (i -> j)
for i in range(len(sequence) - 1):
    current_index = state_to_index[sequence[i]]
    next_index = state_to_index[sequence[i+1]]
    
    count_matrix[current_index, next_index] += 1

print("--- BƯỚC 1: MA TRẬN ĐẾM TẦN SUẤT CHUYỂN ĐỔI ---")
print("Hàng/Cột (theo thứ tự):", states)
print(count_matrix)
print("-" * 50)

# --- 3. TÍNH MA TRẬN XÁC SUẤT CHUYỂN TIẾP (P) ---

P = np.zeros((num_states, num_states))

for i in range(num_states):
    row_sum = count_matrix[i].sum()
    if row_sum > 0:
        P[i] = count_matrix[i] / row_sum
    else:
        # Nếu không có dữ liệu cho trạng thái này, gán xác suất đều
        P[i] = np.ones(num_states) / num_states 

print("--- BƯỚC 2: MA TRẬN XÁC SUẤT CHUYỂN TIẾP (P) ---")
print("Hàng/Cột (theo thứ tự):", states)
print(np.round(P, 4))
print("-" * 50)

# --- 4. DỰ ĐOÁN MÓN ĂN HÔM NAY (1 BƯỚC) ---

# Xác định vector trạng thái ban đầu (π(0))
initial_index = state_to_index[initial_state_name]
initial_vector = np.zeros(num_states)
initial_vector[initial_index] = 1.0

# Dự đoán hôm nay: π(1) = π(0) * P
# initial_vector @ P thực hiện phép nhân ma trận
prediction_today = initial_vector @ P

print("--- BƯỚC 3: DỰ ĐOÁN MÓN ĂN HÔM NAY (π(1)) ---")
print(f"Trạng thái ban đầu: **{initial_state_name}**\n")

results = []
for i, state in enumerate(states):
    results.append((prediction_today[i], state))

# Sắp xếp kết quả theo xác suất giảm dần
results.sort(key=lambda x: x[0], reverse=True)

print("| Món Ăn | Xác Suất Chọn |")
print("| :---: | :---: |")
for prob, state in results:
    print(f"| **{state}** | {prob:.4f} ({prob*100:.2f}%) |")

print("-" * 50)

best_guess = results[0][1]
max_prob = results[0][0]

print(f"DỰ ĐOÁN CUỐI CÙNG:")
print(f"Món ăn hôm nay khả thi nhất là **{best_guess}** (Xác suất {max_prob*100:.2f}%).")