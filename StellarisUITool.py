import re
import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

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
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_icon = Image.open(img_path)
          if img_icon.mode == "RGBA":
            mask = img_icon.split()[3]  # 透過マスクを取得
            image.paste(img_icon, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_icon, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_icon = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_icon, (x, y), img_icon)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_icon = Image.open(img_path)
          if img_icon.mode == "RGBA":
            mask = img_icon.split()[3]  # 透過マスクを取得
            image.paste(img_icon, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_icon, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_icon = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_icon, (x, y), img_icon)

    if element_type == "buttonType":
      x = int(properties["x"])
      y = int(properties["y"])
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_button = Image.open(img_path)
          if img_button.mode == "RGBA":
            mask = img_button.split()[3]  # 透過マスクを取得
            image.paste(img_button, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_button, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_button, (x, y), img_button)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_button = Image.open(img_path)
          if img_button.mode == "RGBA":
            mask = img_button.split()[3]  # 透過マスクを取得
            image.paste(img_button, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_button, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_button, (x, y), img_button)

    if element_type == "effectButtonType":
      x = int(properties["x"])
      y = int(properties["y"])
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_effect_button = Image.open(img_path)
          if img_effect_button.mode == "RGBA":
            mask = img_effect_button.split()[3]  # 透過マスクを取得
            image.paste(img_effect_button, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_effect_button, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_effect_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_effect_button, (x, y), img_effect_button)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_effect_button = Image.open(img_path)
          if img_effect_button.mode == "RGBA":
            mask = img_effect_button.split()[3]  # 透過マスクを取得
            image.paste(img_effect_button, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_effect_button, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_effect_button = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_effect_button, (x, y), img_effect_button)

    if element_type == "overlappingElementsBoxType":
      x = int(properties["x"])
      y = int(properties["y"])
      if "quadTextureSprite" in properties:
        quad_texture_sprite = properties["quadTextureSprite"]
        img_path = f"./img/{quad_texture_sprite}.png"
        if os.path.exists(img_path):
          img_overlapping_elements_box = Image.open(img_path)
          if img_overlapping_elements_box.mode == "RGBA":
            mask = img_overlapping_elements_box.split()[3]  # 透過マスクを取得
            image.paste(img_overlapping_elements_box, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_overlapping_elements_box, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_overlapping_elements_box = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_overlapping_elements_box, (x, y), img_overlapping_elements_box)
      elif "spriteType" in properties:
        sprite_Type = properties["spriteType"]
        img_path = f"./img/{sprite_Type}.png"
        if os.path.exists(img_path):
          img_overlapping_elements_box = Image.open(img_path)
          if img_overlapping_elements_box.mode == "RGBA":
            mask = img_overlapping_elements_box.split()[3]  # 透過マスクを取得
            image.paste(img_overlapping_elements_box, (x, y), mask)  # 透過マスクを適用
          else:
            image.paste(img_overlapping_elements_box, (x, y))
        else:
          print(f"画像が見つかりません: {img_path}")
          img_overlapping_elements_box = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
          image.paste(img_overlapping_elements_box, (x, y), img_overlapping_elements_box)

    if element_type == "instantTextBoxType":
      x = int(properties["x"])
      y = int(properties["y"])
      text = properties["text"]
      if "fontName" in properties:
        font_name = properties["fontName"]
      elif "font" in properties:
        font_name = properties["font"]

      if font_name == "cg_16b":
        font_path = os.path.join("C:\\", "Windows", "Fonts", "arial.ttf")
        font_size = 16
      elif font_name == "malgun_goth_24":
        font_path = os.path.join("C:\\", "Windows", "Fonts", "arial.ttf")
        font_size = 24
      else:
        font_path = os.path.join("C:\\", "Windows", "Fonts", "arial.ttf")
        font_size = 24

      font = ImageFont.truetype(font_path, font_size)
      text_image = Image.new("RGBA", image.size, (255, 255, 255, 0))
      text_draw = ImageDraw.Draw(text_image)
      text_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255))
      image = Image.alpha_composite(image, text_image)

  if background_image:
    if background_image.mode == "RGBA":
      mask = background_image.split()[3]
      image.paste(background_image, (0, 0), mask)
    else:
      image.paste(background_image, (0, 0))

  return image

def show_image():
	code = text_input.get("1.0", "end")
	code = re.sub(r'position\s*=\s*\{', '', code)
	code = re.sub(r'(y\s*=\s*\d+)\s*\}', r'\1', code)
	print(f"Code:\n{code}\n")
	gui_elements = parse_gui_elements(code)
	print(f"GUI Elements:\n{gui_elements}\n")
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

text_input = tk.Text(root, wrap=tk.WORD, width=150, height=75)
text_input.pack(side=tk.LEFT, padx=10, pady=10)

image_listbox = tk.Listbox(root)
image_listbox.pack(side=tk.LEFT, padx=10, pady=10)

image_files = get_image_files()
for image_file in image_files:
  image_listbox.insert(tk.END, image_file)

label = tk.Label(root)
label.pack(side=tk.RIGHT, padx=10, pady=10)

btn = tk.Button(root, text="Analyze", command=show_image)
btn.pack(side=tk.BOTTOM, pady=10)

btn_show_image = tk.Button(root, text="Show Image", command=show_selected_image)
btn_show_image.pack(side=tk.BOTTOM, pady=10)

root.mainloop()