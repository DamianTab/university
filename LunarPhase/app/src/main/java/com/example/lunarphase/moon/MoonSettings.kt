package com.example.lunarphase.moon

import java.io.Serializable


class MoonSettings : Serializable {
    var isNorthSide: Boolean = true
    var algorithm: Algorithm = Algorithm.Simple
}

