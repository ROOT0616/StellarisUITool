import re
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path

def get_system_font_path(font_name):
  system_fonts_path = ""

  if os.name == "nt":
    system_fonts_path = Path("C:/Windows/Fonts")
  elif os.name == "posix":
    system_fonts_path = Path("/usr/share/fonts")

  font_path = system_fonts_path / f"{font_name}.ttf"

  if not font_path.exists():
    font_path = system_fonts_path / "arial.ttf"

  return str(font_path)

def parse_gui_elements(code):
  gui_elements = []

  # Add new element types to this list
  element_types = [
    "containerWindowType",
    "buttonType",
    "effectButtonType",
    "iconType",
    "instantTextBoxType",
    "scrollbarType",
    "extendedScrollbarType",
    "spinnerType",
    "guiButtonType",
    "positionType",
    "listboxType",
    "smoothListboxType",
    "overlappingElementsBoxType",
    "gridBoxType",
    "checkboxType",
    "editBoxType",
    "dropDownBoxType",
    "expandButton",
    "expandedWindow",
    "windowType",
    "background"
  ]

  for element_type in element_types:
    pattern = fr"{element_type}\s+=\s+\{{[\s\S]*?([^}}]+)\s*\}}"
    for match in re.finditer(pattern, code):
      properties = {}
      for prop_match in re.finditer(r"(\w+)\s+=\s+((\{{\s*[^}}]*\s*\}})|(\"[^\"]*\")|(\S+))", match.group(1), re.MULTILINE):
        prop_value = prop_match.group(2).strip()
        if prop_value.startswith('"') and prop_value.endswith('"'):
          prop_value = prop_value[1:-1]
        properties[prop_match.group(1)] = prop_value
      if "position" in properties and "{" in properties["position"] and "}" in properties["position"]:
        properties["position"] = properties["position"].replace("{", "").replace("}", "")
      gui_elements.append((element_type, properties))
  return gui_elements

def generate_image(gui_elements):
  image = Image.new("RGBA", (974, 680), (0, 0, 0, 0))
  draw = ImageDraw.Draw(image)
  background_image = None
  icon_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
  button_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
  effect_button_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
  text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
  icon_images = []  # アイコン画像を保持するリスト
  button_images = []  # ボタン画像を保持するリスト
  text_images = []  # テキスト画像を保持するリスト

  for element_type, properties in gui_elements:
    if element_type == "containerWindowType":
      if "width" in properties and "height" in properties:
        width = int(properties["width"])
        height = int(properties["height"])
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

    if element_type == "background":
      quad_texture_sprite = properties["quadTextureSprite"]
      img_path = f"./img/{quad_texture_sprite}.png"
      if os.path.exists(img_path):
        background_image = Image.open(img_path)
        background_image = background_image.resize((width, height), Image.LANCZOS)
      else:
        print(f"画像が見つかりません: {img_path}")
        background_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

    if element_type == "iconType":
      x = int(properties["x"])
      y = int(properties["y"])
      icon_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_icon = Image.open(img_path)
          if img_icon.mode == "RGBA":
            mask = img_icon.split()[3]  # 透過マスクを取得
            icon_image.paste(img_icon, (x, y), mask)  # 透過マスクを適用
            icon_images.append(icon_image)
          else:
            icon_image.paste(img_icon, (x, y))
            icon_images.append(icon_image)
        else:
          print(f"画像が見つかりません: {img_path}")
          img_icon = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          icon_image.paste(img_icon, (x, y), img_icon)
          icon_images.append(icon_image)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_icon = Image.open(img_path)
          if img_icon.mode == "RGBA":
            mask = img_icon.split()[3]  # 透過マスクを取得
            icon_image.paste(img_icon, (x, y), mask)  # 透過マスクを適用
            icon_images.append(icon_image)
          else:
            icon_image.paste(img_icon, (x, y))
            icon_images.append(icon_image)
        else:
          print(f"画像が見つかりません: {img_path}")
          img_icon = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          icon_image.paste(img_icon, (x, y), img_icon)
          icon_images.append(icon_image)

    if element_type == "buttonType":
      x = int(properties["x"])
      y = int(properties["y"])
      button_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_button = Image.open(img_path)
          if img_button.mode == "RGBA":
            mask = img_button.split()[3]  # 透過マスクを取得
            button_image.paste(img_button, (x, y), mask)  # 透過マスクを適用
            button_images.append(button_image)
          else:
            button_image.paste(img_button, (x, y))
            button_images.append(button_image)
        else:
          print(f"画像が見つかりません: {img_path}")
          img_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          button_image.paste(img_button, (x, y), img_button)
          button_images.append(button_image)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_button = Image.open(img_path)
          if img_button.mode == "RGBA":
            mask = img_button.split()[3]  # 透過マスクを取得
            button_image.paste(img_button, (x, y), mask)  # 透過マスクを適用
            button_images.append(button_image)
          else:
            button_image.paste(img_button, (x, y))
            button_images.append(button_image)
        else:
          print(f"画像が見つかりません: {img_path}")
          img_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          button_image.paste(img_button, (x, y), img_button)
          button_images.append(button_image)

    if element_type == "instantTextBoxType":
      x = int(properties["x"])
      y = int(properties["y"])
      text = properties["text"]
      if "fontName" in properties:
        font_name = properties["fontName"]
      elif "font" in properties:
        font_name = properties["font"]

      if font_name == "cg_16b":
        font_path = get_system_font_path("arial")
        font_size = 16
      elif font_name == "malgun_goth_24":
        font_path = get_system_font_path("arial")
        font_size = 24
      else:
        font_path = get_system_font_path("arial")
        font_size = 24

      font = ImageFont.truetype(font_path, font_size)
      text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
      text_images.append(text_image)
      text_draw = ImageDraw.Draw(text_image)
      text_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))

  if background_image:
    if background_image.mode == "RGBA":
      mask = background_image.split()[3]
      image.paste(background_image, (0, 0), mask)
    else:
      image.paste(background_image, (0, 0))

  # テキスト画像をすべて合成
  for text_image in text_images:
    image = Image.alpha_composite(image, text_image)
  # アイコン画像をすべて合成
  for icon_image in icon_images:
    image = Image.alpha_composite(image, icon_image)
  # ボタン画像をすべて合成
  for button_image in button_images:
    image = Image.alpha_composite(image, button_image)

  return image


def zoom_image(scale):  # 新しい関数 - 画像をズームする
  global current_image
  if current_image is not None:
    new_width = int(current_image.width * scale)
    new_height = int(current_image.height * scale)
    resized_image = current_image.resize((new_width, new_height), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_image)
    label.config(image=tk_image)
    label.image = tk_image

def show_image():
  global current_image
  code = text_input.get("1.0", "end")
  code = re.sub(r'position\s*=\s*\{', '', code)
  code = re.sub(r'(y\s*=\s*\d+)\s*\}', r'\1', code)
  print(f"Code:\n{code}\n")
  gui_elements = parse_gui_elements(code)
  print(f"GUI Elements:\n{gui_elements}\n")
  current_image = generate_image(gui_elements)
  image = generate_image(gui_elements)

  tk_image = ImageTk.PhotoImage(image)
  label.config(image=tk_image)
  label.image = tk_image

def get_image_files():
  img_dir = "img"
  image_files = [os.path.join(img_dir, f) for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f)) and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
  return image_files

def show_selected_image():
  selected_image = image_listbox.get(image_listbox.curselection())
  img_path = selected_image
  image = Image.open(img_path)
  tk_image = ImageTk.PhotoImage(image)
  label.config(image=tk_image)
  label.image = tk_image

root = tk.Tk()
root.title("GUI Analyzer")

frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, padx=10, pady=10)

text_input = tk.Text(frame_left, wrap=tk.NONE, width=100, height=80)
text_input.grid(row=0, column=0, padx=(0, 10))

text_scrollbar = tk.Scrollbar(frame_left, orient=tk.HORIZONTAL, command=text_input.xview)
text_scrollbar.grid(row=1, column=0, sticky=tk.EW)
text_input.config(xscrollcommand=text_scrollbar.set)

frame_middle = tk.Frame(root)
frame_middle.pack(side=tk.LEFT, padx=10, pady=10)

image_listbox = tk.Listbox(frame_middle, width=30, height=30)
image_listbox.pack(side=tk.LEFT, padx=(0, 10))

frame_right = tk.Frame(root)
frame_right.pack(side=tk.RIGHT, padx=10, pady=10)

label = tk.Label(frame_right, bg="SystemButtonFace")
label.pack(side=tk.TOP, padx=10, pady=10)

btn_zoom_in = tk.Button(frame_right, text="Zoom In", command=lambda: zoom_image(1.5))
btn_zoom_in.pack(side=tk.BOTTOM, pady=5)

btn_zoom_out = tk.Button(frame_right, text="Zoom Out", command=lambda: zoom_image(0.8))
btn_zoom_out.pack(side=tk.BOTTOM, pady=5)

btn = tk.Button(frame_right, text="Analyze", command=show_image)
btn.pack(side=tk.BOTTOM, pady=10)

btn_show_image = tk.Button(frame_middle, text="Show Image", command=show_selected_image)
btn_show_image.pack(side=tk.BOTTOM, pady=10)

image_files = get_image_files()
for image_file in image_files:
  image_listbox.insert(tk.END, image_file)

root.mainloop()