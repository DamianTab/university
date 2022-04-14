package com.example.lunarphase.moon

import android.os.Build
import androidx.annotation.RequiresApi
import java.time.LocalDate
import java.time.LocalDateTime
import java.time.ZoneOffset
import kotlin.math.ceil
import kotlin.math.floor
import kotlin.math.sin
import kotlin.reflect.KFunction4

/**
 *
 * Algorithms were copied from http://ben-daglish.net/moon.shtml
 * That's why they look ugly :)
 *
 */

enum class Algorithm {
    Simple(Algorithm::simple), Conway(
        Algorithm::conway
    ),
    Trig1(Algorithm::trig1), Trig2(
        Algorithm::trig2
    );

    private val function: KFunction4<Algorithm, Int, Int, Int, Double>

    constructor(
        func: KFunction4<Algorithm, @ParameterName(name = "year") Int, @ParameterName(
            name = "month"
        ) Int, @ParameterName(name = "day") Int, Double>
    ) {
        this.function = func
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun calculate(date: LocalDate): Double {

        return function(this, date.year, date.monthValue, date.dayOfMonth)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun simple(year: Int, month: Int, day: Int): Double {
        val lp = 2551443
        val now = LocalDateTime.of(year, month, day, 20, 35, 0).atZone(ZoneOffset.UTC).toInstant()
            .toEpochMilli()
        val newMoon = LocalDateTime.of(1970, 1, 7, 20, 35, 0).atZone(ZoneOffset.UTC).toInstant()
            .toEpochMilli()
        val phase = ((now - newMoon) / 1000) % lp
        return floor(phase / (24 * 3600).toDouble()) + 1
    }

    private fun conway(year: Int, month: Int, day: Int): Double {
        var r = year % 100.0
        r %= 19
        if (r > 9) {
            r -= 19
        }
        r = ((r * 11) % 30) + month + day
        if (month < 3) {
            r += 2
        }
        r -= if (year < 2000) 4.0 else 8.3
        r = floor(r + 0.5) % 30
        return if (r < 0) r + 30 else r
    }

    private fun trig1(year: Int, month: Int, day: Int): Double {
        val thisJD = julday(year, month, day)
        val degToRad = 3.14159265 / 180
        val K0 = floor((year - 1900) * 12.3685)
        val T = (year - 1899.5) / 100
        val T2 = T * T
        val T3 = T * T * T
        val J0 = 2415020 + 29 * K0
        val F0 =
            0.0001178 * T2 - 0.000000155 * T3 + (0.75933 + 0.53058868 * K0) - (0.000837 * T + 0.000335 * T2)
        val M0 =
            360 * (getFraction(K0 * 0.08084821133)) + 359.2242 - 0.0000333 * T2 - 0.00000347 * T3
        val M1 =
            360 * (getFraction(K0 * 0.07171366128)) + 306.0253 + 0.0107306 * T2 + 0.00001236 * T3
        val B1 =
            360 * (getFraction(K0 * 0.08519585128)) + 21.2964 - (0.0016528 * T2) - (0.00000239 * T3)
        var phase = 0.0
        var jday = 0.0
        var oldJ = 0.0
        while (jday < thisJD) {
            var F = F0 + 1.530588 * phase
            val M5 = (M0 + phase * 29.10535608) * degToRad
            val M6 = (M1 + phase * 385.81691806) * degToRad
            val B6 = (B1 + phase * 390.67050646) * degToRad
            F -= 0.4068 * sin(M6) + (0.1734 - 0.000393 * T) * sin(M5)
            F += 0.0161 * sin(2 * M6) + 0.0104 * sin(2 * B6)
            F -= 0.0074 * sin(M5 - M6) - 0.0051 * sin(M5 + M6)
            F += 0.0021 * sin(2 * M5) + 0.0010 * sin(2 * B6 - M6)
            F += 0.5 / 1440
            oldJ = jday
            jday = J0 + 28 * phase + floor(F)
            phase++
        }
        return (thisJD - oldJ) % 30

    }

    private fun trig2(year: Int, month: Int, day: Int): Double {
        val n = floor(12.37 * (year - 1900 + ((1.0 * month - 0.5) / 12.0)))
        val RAD = 3.14159265 / 180.0
        val t = n / 1236.85
        val t2 = t * t
        val as1 = 359.2242 + 29.105356 * n
        val am = 306.0253 + 385.816918 * n + 0.010730 * t2
        var xtra = 0.75933 + 1.53058868 * n + ((1.178e-4) - (1.55e-7) * t) * t2
        xtra += (0.1734 - 3.93e-4 * t) * sin(RAD * as1) - 0.4068 * sin(RAD * am)
        val i = if (xtra > 0.0) floor(xtra) else ceil(xtra - 1.0)
        val j1 = julday(year, month, day)
        val jd = (2415020 + 28 * n) + i
        return (j1 - jd + 30) % 30
    }

    private fun julday(year: Int, month: Int, day: Int): Double {
        var year = year
        if (year < 0) {
            year++;
        }
        var jy = year
        var jm = month + 1
        if (month <= 2) {
            jy--
            jm += 12
        }
        var jul = floor(365.25 * jy) + floor(30.6001 * jm) + day + 1720995;
        if (day + 31 * (month + 12 * year) >= (15 + 31 * (10 + 12 * 1582))) {
            val ja = floor(0.01 * jy);
            jul = jul + 2 - ja + floor(0.25 * ja);
        }
        return jul;
    }

    private fun getFraction(fr: Double): Double {
        return (fr - floor(fr));
    }
}