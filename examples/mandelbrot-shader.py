# Mandelbrot set, computed per-pixel on the GPU.
# A GLSL fragment shader on a SpriteNode ignores the sprite's texture and
# colors each pixel from v_tex_coord instead.
# Source: community Pythonista-Tools collection (Andrew4200/Pythonista).
from scene import *

SHADER_SRC = '''
precision highp float;
varying vec2 v_tex_coord;

int mandelbrot(vec2 uv) {
    vec2 z = vec2(0.0, 0.0);
    for (int i = 0; i < 64; i++) {
        if (dot(z, z) > 4.0) return i;  // |z| > 2 escapes; dot() avoids sqrt
        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + uv;
    }
    return 0;
}

vec3 make_color(int i) {
    if (i == 0)       return vec3(0.0, 0.0, 0.0);
    else if (i < 64)  return vec3(float(i * 4 + 128), float(i * 4), 0.0) / 255.0;
    else if (i < 128) return vec3(64.0, 255.0, float((i - 64) * 4)) / 255.0;
    else if (i < 192) return vec3(64.0, float(255 - (i - 128) * 4), 255.0) / 255.0;
    else              return vec3(64.0, 0.0, float(255 - (i - 192) * 4)) / 255.0;
}

void main(void) {
    vec2 uv = vec2((v_tex_coord.x - 0.65) * 4.0, (v_tex_coord.y - 0.5) * 4.0);
    gl_FragColor = vec4(make_color(mandelbrot(uv)), 1.0);
}
'''


class MandelbrotScene(Scene):
    def setup(self):
        side = min(self.size.w, self.size.h)
        sprite = SpriteNode('plf:Enemy_Bee_move', size=(side, side),
                            position=self.size / 2, parent=self)
        sprite.shader = Shader(SHADER_SRC)


run(MandelbrotScene())
