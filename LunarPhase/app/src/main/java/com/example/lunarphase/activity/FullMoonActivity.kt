package com.example.lunarphase.activity

import android.graphics.Color
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.example.lunarphase.R
import com.example.lunarphase.moon.Algorithm
import com.example.lunarphase.moon.MoonSettings
import com.example.lunarphase.utils.Utils
import kotlinx.android.synthetic.main.activity_full_moon.*
import java.time.LocalDate
import kotlin.math.round

class FullMoonActivity : AppCompatActivity() {

    private var moonSettings: MoonSettings? = null
    private var cellList: List<TextView>? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_full_moon)
        moonSettings = intent.extras?.get(Utils.Data.toString()) as MoonSettings?
        cellList = listOf(
            cell,
            cell1,
            cell2,
            cell3,
            cell4,
            cell5,
            cell6,
            cell7,
            cell8,
            cell9,
            cell10,
            cell11
        )
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun fullMoonsInYear(view: View) {
        if (yearInput.text.toString() == "") return
        val year = yearInput.text.toString().toInt()
        if (year > 2200 || year < 1900) {
            yearInput.setTextColor(Color.RED)
            Toast.makeText(this, "Year have to be between 1900-2200", Toast.LENGTH_SHORT).show()
        } else if (year < 1970 && moonSettings!!.algorithm == Algorithm.Simple) {
            Toast.makeText(
                this,
                "With Simple algorithm you have to choose year from 1970 onwards",
                Toast.LENGTH_SHORT
            ).show()
        } else if ((year > 2099 || year < 2000) && moonSettings!!.algorithm == Algorithm.Conway) {
            Toast.makeText(
                this,
                "With Conway algorithm you have to choose year between 2000-2099",
                Toast.LENGTH_SHORT
            ).show()
        } else {
            yearInput.setTextColor(Color.BLACK)
            val date = LocalDate.of(year, 1, 1)
            var fullMoonDate = findFullMoon(date)

            cellList!!.stream()
                .takeUnless { fullMoonDate.year != year }
                ?.forEach {
                    it.text = fullMoonDate.toString()
                    fullMoonDate = fullMoonDate.plusDays(2)
                    fullMoonDate = findFullMoon(fullMoonDate)
                }
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun findFullMoon(date: LocalDate): LocalDate {
        val phaseDay = moonSettings!!.algorithm.calculate(date)
        return if (phaseDay <= 15) {
            date.plusDays(15 - phaseDay.toLong())
        } else {
            date.plusDays(30 - phaseDay.toLong() + 15)
        }
    }
}
