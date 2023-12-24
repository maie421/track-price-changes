import cv2
from skimage import io

def compare_images(image1_path, image2_path):
    # 이미지 불러오기
    image1 = io.imread(image1_path)
    image2 = io.imread(image2_path)

    # 이미지 크기 조정
    image1 = cv2.resize(image1, (300, 300))
    image2 = cv2.resize(image2, (300, 300))

    # 이미지를 그레이스케일로 변환
    image1_gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2_gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

    # 히스토그램 계산
    hist1 = cv2.calcHist([image1_gray], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([image2_gray], [0], None, [256], [0, 256])

    # 히스토그램 비교
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    return similarity

image1_path = 'https://thumbnail9.coupangcdn.com/thumbnails/remote/230x230ex/image/rs_quotation_api/syffhz5g/1d3d5359a7dc42f58fc21fd671240380.jpg'
image2_path = 'https://thumbnail10.coupangcdn.com/thumbnails/remote/230x230ex/image/rs_quotation_api/5dri148t/2c11d3803e1a4a729058a6968ac05724.jpg'

specific_image_path = image1_path

image_paths = {
    'image1': image2_path,
    'image2': 'http://thumbnail8.coupangcdn.com/thumbnails/remote/230x230ex/image/retail/images/6880754174896457-655cf936-e389-4cd9-8e1d-a49e3224436d.jpg',
    'image3': 'http://thumbnail7.coupangcdn.com/thumbnails/remote/230x230ex/image/retail/images/234770817353279-c3f30906-ffbe-48a5-baec-4ce59d17fbc9.jpg',
}

similarity_scores = {}

for key, path in image_paths.items():
    similarity_score = compare_images(specific_image_path, path)
    similarity_scores[key] = similarity_score

selected_keys = [key for key, score in similarity_scores.items() if score > 0.8]

print(f"Keys with similarity score greater than 5: {selected_keys}")
