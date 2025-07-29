try:
    # 尝试导入最新 ComfyUI 结构
    from comfy import nodes
except ImportError:
    # 兼容较旧版本
    try:
        from nodes import Node
    except ImportError:
        # 兼容未知版本（定义空基类）
        class Node:
            pass

# T:\dapao_ComfyUI\ComfyUI\custom_nodes\CropBoxCalculator\crop_box_calculator.py

class CropBoxCalculatorNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "x": ("INT", {"default": 100, "min": 0, "step": 1, "label": "X 坐标"}),
                "y": ("INT", {"default": 100, "min": 0, "step": 1, "label": "Y 坐标"}),
                "width": ("INT", {"default": 200, "min": 1, "step": 1, "label": "宽度"}),
                "height": ("INT", {"default": 200, "min": 1, "step": 1, "label": "高度"}),
                # 自定义倍数参数，可在所有公式中灵活使用
                "multiplier": ("FLOAT", {"default": 2.0, "min": 0.1, "max": 20.0, "step": 0.1, "label": "自定义倍数"}),
            },
            "optional": {
                # 公式示例中展示多种multiplier用法
                "formula_x": ("STRING", {"default": "x * multiplier", "label": "X公式 (支持 x, y, w, h, multiplier)"}),
                "formula_y": ("STRING", {"default": "y + multiplier * 10", "label": "Y公式"}),
                "formula_w": ("STRING", {"default": "w * (multiplier / 2)", "label": "宽度公式"}),
                "formula_h": ("STRING", {"default": "h + (multiplier - 1) * 50", "label": "高度公式"}),
            }
        }

    RETURN_TYPES = ("INT_LIST",)
    RETURN_NAMES = ("crop_box",)  # 输出[x1, y1, x2, y2]格式
    FUNCTION = "run"
    CATEGORY = "custom/crop"

    def run(self, x, y, width, height, multiplier, 
            formula_x="x * multiplier", formula_y="y + multiplier * 10", 
            formula_w="w * (multiplier / 2)", formula_h="h + (multiplier - 1) * 50"):
        try:
            # 将所有可用变量注入公式上下文
            context = {
                "x": x,          # 原始X坐标
                "y": y,          # 原始Y坐标
                "w": width,      # 原始宽度
                "h": height,     # 原始高度
                "multiplier": multiplier  # 自定义倍数参数
            }
            
            # 计算公式并转换为整数
            x_new = int(eval(formula_x, {"__builtins__": None}, context))
            y_new = int(eval(formula_y, {"__builtins__": None}, context))
            w_new = int(eval(formula_w, {"__builtins__": None}, context))
            h_new = int(eval(formula_h, {"__builtins__": None}, context))

            # 输出裁剪框格式 [x1, y1, x2, y2]
            crop_box = [x_new, y_new, x_new + w_new, y_new + h_new]
            return (crop_box,)

        except Exception as e:
            print(f"公式计算错误: {str(e)}")
            return ([x, y, x + width, y + height],)  # 错误时返回原始值
            
            
NODE_CLASS_MAPPINGS = {
    "CropBoxCalculator": CropBoxCalculatorNode
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "CropBoxCalculator": "CropBox 自定义计算器（适配裁剪框）"
}
