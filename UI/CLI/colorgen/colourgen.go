package colorgen

import (
    "fmt"
    "math/rand"
	"math"
)

func hslToHex(h, s, l float64) string {
    c := (1 - abs(2*l-1)) * s
    x := c * (1 - abs(math.Mod(h/60, 2)-1))
    m := l - c/2

    var r, g, b float64
    switch {
    case 0 <= h && h < 60:
        r, g, b = c, x, 0
    case 60 <= h && h < 120:
        r, g, b = x, c, 0
    case 120 <= h && h < 180:
        r, g, b = 0, c, x
    case 180 <= h && h < 240:
        r, g, b = 0, x, c
    case 240 <= h && h < 300:
        r, g, b = x, 0, c
    case 300 <= h && h < 360:
        r, g, b = c, 0, x
    }

    ri := int((r + m) * 255)
    gi := int((g + m) * 255)
    bi := int((b + m) * 255)

    return fmt.Sprintf("#%02x%02x%02x", ri, gi, bi)
}

func abs(x float64) float64 {
    if x < 0 {
        return -x
    }
    return x
}

func RandomBrightHex() string {
    hue := rand.Float64() * 360
    saturation := 0.7 + rand.Float64()*0.3
    lightness := 0.5 + rand.Float64()*0.25
    return hslToHex(hue, saturation, lightness)
}

// func GenerateRandomGradientHex() (string, string) {
//     baseHue := rand.Float64() * 360
//
//     saturation := 0.8 + rand.Float64()*0.2
//     lightness := 0.55 + rand.Float64()*0.15
//
//     hueShift := 35.0 + rand.Float64()*30.0
//     secondHue := math.Mod(baseHue+hueShift, 360)
//
//     color1 := hslToHex(baseHue, saturation, lightness)
//     color2 := hslToHex(secondHue, saturation, lightness)
//
//     return color1, color2
// }
