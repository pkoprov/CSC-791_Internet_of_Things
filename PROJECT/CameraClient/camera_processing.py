import cv2
import numpy as np
import time
from cv2 import threshold

prev_grid = np.zeros((6, 7))
reset = False
reset_counter = 0
counter_condition1 = 0
counter_condition2 = 0
counter_condition3 = 0

threshold = 50


def displaying_image(name, image):
    cv2.imshow(name, image)
    # cv2.moveWindow(name, 200, 200)
    # cv2.waitKey(0)


def convertBoardToString(board):
    board_string = ""
    for i in range(6):
        for j in range(7):
            if board[i][j] == 0:
                board_string += "#"
            elif board[i][j] == 1:
                board_string += "O"
            elif board[i][j] == -1:
                board_string += "X"
        board_string += "\n"
    return board_string


def checkForEmpty(board):
    for i in range(6):
        for j in range(7):
            if board[i][j] != 0:
                return False
    return True


def generate_grid(image):
    global prev_grid, reset, reset_counter, counter_condition1, counter_condition2, counter_condition3
    image = image[10:400, 50:600]
    new_width_for_resizing = 400  # Resize
    height_of_Image, width_of_image, _ = image.shape
    scale = new_width_for_resizing / width_of_image
    height_of_Image = int(height_of_Image * scale)
    width_of_image = int(width_of_image * scale)
    image = cv2.resize(image, (width_of_image, height_of_Image),
                       interpolation=cv2.INTER_AREA)
    img_orig = image.copy()
    # self.displaying_image('(Resized) Orignal Image', img_orig)
    # Applying Bilateral to remove the noise from the Background
    filtered_image = cv2.bilateralFilter(image, 15, 190, 190)
    # self.displaying_image('Bilateral Filter',filtered_image)
    # Outlining the  Edges
    detected_edge_image = cv2.Canny(filtered_image, 75, 150)
    # self.displaying_image('Edge Detection', detected_edge_image)
    # Find the Circles
    contours, hierarchy = cv2.findContours(
        detected_edge_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Edges to contours
    list_of_contours = []
    list_of_rect = []
    list_of_position = []
    for contour in contours:
        approximate = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)  # Contour Polygons
        area_of_countour = cv2.contourArea(contour)
        countour_rect = cv2.boundingRect(
            contour)  # Polygon bounding rectangles
        rect_x, rect_y, rect_w, rect_h = countour_rect
        rect_x += rect_w / 2
        rect_y += rect_h / 2
        area_rect = rect_w * rect_h
        if ((len(approximate) > 8) & (len(approximate) < 23) & (area_of_countour > 250) & (
                area_rect < (width_of_image * height_of_Image) / 5)) & (
                rect_w in range(rect_h - 10, rect_h + 10)):  # Circle conditions
            list_of_contours.append(contour)
            list_of_position.append((rect_x, rect_y))
            list_of_rect.append(countour_rect)

    circle_contours_img = img_orig.copy()
    cv2.drawContours(circle_contours_img, list_of_contours, -1,
                     (0, 255, 0), thickness=1)  # Display Circles
    for countour_rect in list_of_rect:
        x, y, w, h = countour_rect
        cv2.rectangle(circle_contours_img, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # self.displaying_image('Detected Circles',circle_contours_img)

    # Interpolating  Grid using the Detected Circle
    rows, columns = (6, 7)
    if len(list_of_rect) == 0:
        return
    w_mean = sum([countour_rect[2] for r in list_of_rect]) / len(list_of_rect)
    h_mean = sum([countour_rect[3] for r in list_of_rect]) / len(list_of_rect)
    list_of_position.sort(key=lambda x: x[0])
    x_max = int(list_of_position[-1][0])
    x_min = int(list_of_position[0][0])
    list_of_position.sort(key=lambda x: x[1])
    y_max = int(list_of_position[-1][1])
    y_min = int(list_of_position[0][1])
    width_grid = x_max - x_min
    height_grid = y_max - y_min
    spacing_col = int(width_grid / (columns - 1))
    spacing_row = int(height_grid / (rows - 1))

    # Finding the  Colour Masks
    # Convert to the HSV space
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # lower boundary RED color range values; Hue (0 - 10)
    lower_1 = np.array([0, 100, 20])
    upper_1 = np.array([10, 255, 255])
    # upper boundary RED color range values; Hue (160 - 180)
    lower_2 = np.array([160, 100, 20])
    upper_2 = np.array([179, 255, 255])
    lower_mask = cv2.inRange(img_hsv, lower_1, upper_1)
    upper_mask = cv2.inRange(img_hsv, lower_2, upper_2)
    Complete_mask = lower_mask + upper_mask
    img_red = cv2.bitwise_and(image, image, mask=Complete_mask)
    # self.displaying_image("Red Mask",img_red)
    lower_yellow = np.array([22, 93, 0])
    upper_yellow = np.array([45, 255, 255])
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    img_yellow = cv2.bitwise_and(image, image, mask=mask_yellow)
    # self.displaying_image("Yellow Mask",img_yellow)
    Calculated_grid = np.zeros((rows, columns))
    id_of_red = 1
    id_of_yellow = -1
    overlay_img_grid = img_orig.copy()
    grid_img = np.zeros([height_of_Image, width_of_image, 3], dtype=np.uint8)
    for i in range(0, columns):
        x = int(x_min + i * spacing_col)
        for y_i in range(0, rows):
            y = int(y_min + y_i * spacing_row)
            r = int((h_mean + w_mean) / 5)
            circle_img_grid_ = np.zeros((height_of_Image, width_of_image))
            cv2.circle(circle_img_grid_, (x, y), r,
                       (255, 255, 255), thickness=-1)
            img_res_red = cv2.bitwise_and(
                circle_img_grid_, circle_img_grid_, mask=Complete_mask)
            circle_img_grid_ = np.zeros((height_of_Image, width_of_image))
            cv2.circle(circle_img_grid_, (x, y), r,
                       (255, 255, 255), thickness=-1)
            img_res_yellow = cv2.bitwise_and(
                circle_img_grid_, circle_img_grid_, mask=mask_yellow)
            cv2.circle(overlay_img_grid, (x, y), r, (0, 255, 0), thickness=1)
            if img_res_red.any() != 0:
                Calculated_grid[y_i][i] = id_of_red
                cv2.circle(grid_img, (x, y), r, (0, 0, 255), thickness=-1)
            elif img_res_yellow.any() != 0:
                Calculated_grid[y_i][i] = id_of_yellow
                cv2.circle(grid_img, (x, y), r, (0, 255, 255), thickness=-1)

    # Place the yellow and red masks side by side
    img_grid = np.hstack((img_red, img_yellow))
    overlay_img_grid = np.hstack((overlay_img_grid, grid_img))
    overlay_img_grid = np.hstack((overlay_img_grid, image))
    displaying_image('Camera Results', overlay_img_grid)

    # print(Calculated_grid)
    freq_yellow = 0
    freq_red = 0
    for i in range(0, 6):
        for j in range(0, 7):
            if i + 1 <= 5 and (Calculated_grid[i][j] == 1 or Calculated_grid[i][j] == -1):
                if Calculated_grid[i + 1][j] == 0:
                    # print("Not a valid Grid")
                    return
    for i in range(0, 6):
        for j in range(0, 7):
            if Calculated_grid[i][j] == -1:
                freq_yellow += 1
            if Calculated_grid[i][j] == 1:
                freq_red += 1

    if np.all((Calculated_grid == 0)):
        if reset_counter == 100 and not reset:
            # reset = True
            reset_counter = 0
            return "RESET"
        reset_counter += 1
    if abs(freq_red - freq_yellow) > 1:
        if counter_condition1 == threshold:
            counter_condition1 = 0
            return
        counter_condition1 += 1
    if freq_red + freq_yellow > 42:
        if counter_condition2 == threshold:
            counter_condition2 = 0
            return
        counter_condition2 += 1
        return
    if np.array_equal(prev_grid, Calculated_grid) == False:
        if counter_condition3 == threshold:
            counter_condition3 = 0
            prev_grid = Calculated_grid
            if checkForEmpty(Calculated_grid) == True:
                reset = False
                return
            else:
                reset = False
                return convertBoardToString(Calculated_grid)
        counter_condition3 += 1


if __name__ == '__main__':
    cap = cv2.VideoCapture(1)
    while (True):
        ret, frame = cap.read()

        # Our operations on the frame come here
        if not ret:
            print("No Image Found!")
            continue
        cropped_image = frame[10:400, 50:600]
        generate_grid(cropped_image)
        cv2.imshow("image", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
