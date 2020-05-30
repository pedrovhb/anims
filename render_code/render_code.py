from io import BytesIO

from manim import *
from pygments import highlight
from pygments.lexers.python import Python3Lexer

from render_code.custom_formatter import TransparentImageFormatter
from render_code.dracula import DraculaStyle

MEDIA_ROOT = r"C:\Users\Pedro\PycharmProjects\anims\media"
IMAGES_ROOT = os.path.join(MEDIA_ROOT, "code_images")


class RenderedCode:
    RENDER_FONT = "JetBrains Mono"
    LINE_NUMBER_PAD = 14
    LINE_HEIGHT_CONSTANT = 1.8
    HIGHLIGHT_RECT_HEIGHT_CONSTANT = 0.8
    FILE_EXT = ".png"

    def __init__(
            self, code: str, font_size=48, image_pad=12, scale=0.15, use_line_numbers=True
    ):
        self.use_line_numbers = use_line_numbers
        self.font_size = font_size
        self.image_pad = image_pad
        self.scale = scale

        self.lexer = Python3Lexer()
        self.style = DraculaStyle

        self.code_lines = code.split("\n")

        self.image_paths = []
        self.group = Group()

        self._render_lines()
        self._adjust_size()
        self._max_line_width = 0

    @classmethod
    def from_file(cls, file_path, font_size=48, image_pad=12, scale=0.15):
        with open(file_path) as fd:
            code = fd.read()
        return cls(code, font_size, image_pad, scale)

    @property
    def line_mobjects(self):
        return self.group.submobjects

    def _adjust_size(self):
        for i, line in enumerate(self.group.submobjects):
            line.shift(DOWN * i * self.LINE_HEIGHT_CONSTANT)
            line.align_to(self.group, LEFT)
        self.group.scale(self.scale)

    def _render_lines(self):

        if not os.path.isdir(IMAGES_ROOT):
            os.mkdir(IMAGES_ROOT)

        for i, line in enumerate(self.code_lines):
            file_path = self._render_line(line, i + 1)
            self.image_paths.append(file_path)
            self.group.add(ImageMobject(file_path))

    def _render_line(self, line, line_no=0):
        file_name = hashlib.md5(line.encode()).hexdigest()
        file_name += self.FILE_EXT
        file_path = os.path.join(IMAGES_ROOT, file_name)

        if os.path.isfile(file_path):
            return file_path

        lexer = self.lexer
        formatter = TransparentImageFormatter(
            font_name=self.RENDER_FONT,
            style=self.style,
            image_pad=self.image_pad,
            font_size=self.font_size,
            line_numbers=self.use_line_numbers,
            line_number_bg="#29395200",
            line_number_fg="#CCCCDD",
            line_number_pad=self.LINE_NUMBER_PAD,
            line_number_start=line_no,
            line_number_separator=False,
        )
        with open(file_path, "wb") as fd:
            highlight(line, lexer, formatter, fd)
        return file_path


class RenderedCodeWithHighlight(RenderedCode):
    HIGHLIGHT_COLOR = "#40577a"

    def __init__(
            self, code, font_size=48, image_pad=12, scale=0.15, use_line_numbers=True
    ):
        self.highlight_rect = Rectangle()
        super(RenderedCodeWithHighlight, self).__init__(
            code,
            font_size=font_size,
            image_pad=image_pad,
            scale=scale,
            use_line_numbers=use_line_numbers,
        )

        self.highlight_rect.set_height(self.line_mobjects[0].get_height() * self.HIGHLIGHT_RECT_HEIGHT_CONSTANT)
        self.highlight_rect.set_width(self.group.get_width(), stretch=True)

        self.highlight_rect.set_color(self.HIGHLIGHT_COLOR)
        self.highlight_rect.set_fill(self.HIGHLIGHT_COLOR, 1)

        # self.group.add(self.highlight_rect)
        self.highlight_rect.align_to(self.group, LEFT)
        self.highlight_rect.align_to(self.line_mobjects[0], DOWN)

    def _adjust_size(self):
        self.highlight_rect.align_to(self.group, LEFT)
        super()._adjust_size()

    def animate_highlight_line(self, line_number):
        line_index = line_number - 1
        self.highlight_rect.align_to(self.group, LEFT)
        return ApplyFunction(
            lambda ob: ob.align_to(self.line_mobjects[line_index], DOWN),
            self.highlight_rect,
        )
