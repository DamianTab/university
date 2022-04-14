package com.example.lunarphase.moon

import com.example.lunarphase.R
import kotlin.math.round

class PhotoManager {

    private val northBeginningPhasePhotos: List<Int> = listOf(
        R.drawable.n_b_0_4,
        R.drawable.n_b_2_8,
        R.drawable.n_b_7_3,
        R.drawable.n_b_13_5,
        R.drawable.n_b_21,
        R.drawable.n_b_29_5,
        R.drawable.n_b_38_6,
        R.drawable.n_b_48,
        R.drawable.n_b_57_4,
        R.drawable.n_b_66_7,
        R.drawable.n_b_75_4,
        R.drawable.n_b_83_3,
        R.drawable.n_b_90,
        R.drawable.n_b_95_3,
        R.drawable.n_b_98_7
    )
    private val northEndingPhasePhotos: List<Int> = listOf(
        R.drawable.n_e_0_1,
        R.drawable.n_e_1_2,
        R.drawable.n_e_4_5,
        R.drawable.n_e_10,
        R.drawable.n_e_17_5,
        R.drawable.n_e_26_8,
        R.drawable.n_e_37_3,
        R.drawable.n_e_48_6,
        R.drawable.n_e_60,
        R.drawable.n_e_71,
        R.drawable.n_e_80_8,
        R.drawable.n_e_89,
        R.drawable.n_e_95,
        R.drawable.n_e_98_7,
        R.drawable.n_e_99_9
    )
    private val southBeginningPhasePhotos: List<Int> = listOf(
        R.drawable.s_b_0_1,
        R.drawable.s_b_1_4,
        R.drawable.s_b_5_4,
        R.drawable.s_b_11_7,
        R.drawable.s_b_19_7,
        R.drawable.s_b_28_9,
        R.drawable.s_b_38_7,
        R.drawable.s_b_48_7,
        R.drawable.s_b_58_5,
        R.drawable.s_b_67_7,
        R.drawable.s_b_76_2,
        R.drawable.s_b_83_8,
        R.drawable.s_b_90_1,
        R.drawable.s_b_95,
        R.drawable.s_b_98_3,
        R.drawable.s_b_99_8
    )
    private val southEndingPhasePhotos: List<Int> = listOf(
        R.drawable.s_e_0_1,
        R.drawable.s_e_0_2,
        R.drawable.s_e_0_4,
        R.drawable.s_e_3,
        R.drawable.s_e_8_3,
        R.drawable.s_e_15_9,
        R.drawable.s_e_25_4,
        R.drawable.s_e_36_1,
        R.drawable.s_e_47_4,
        R.drawable.s_e_58_5,
        R.drawable.s_e_69_1,
        R.drawable.s_e_78_5,
        R.drawable.s_e_86_4,
        R.drawable.s_e_92_7,
        R.drawable.s_e_97,
        R.drawable.s_e_99_4
    )

    fun receivePhotoId(phaseDay: Double, isNorthSide: Boolean): Int {
        return if (phaseDay <= 15) {
            if (isNorthSide) {
                northBeginningPhasePhotos[normalizeLength(phaseDay, northBeginningPhasePhotos)]
            } else {
                southBeginningPhasePhotos[normalizeLength(phaseDay, southBeginningPhasePhotos)]
            }
        } else {
            if (isNorthSide) {
                northEndingPhasePhotos[normalizeLength(phaseDay, northEndingPhasePhotos)]
            } else {
                southEndingPhasePhotos[normalizeLength(phaseDay, southEndingPhasePhotos)]
            }
        }
    }

    private fun normalizeLength(phaseDay: Double, list: List<Int>): Int {
        return round(phaseDay / 29 * list.size).toInt()
    }
}