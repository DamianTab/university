package com.example.lunarphase.activity

import android.app.Activity
import android.content.Intent
import android.os.Build
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.example.lunarphase.R
import com.example.lunarphase.moon.MoonSettings
import com.example.lunarphase.moon.PhotoManager
import com.example.lunarphase.utils.Utils
import kotlinx.android.synthetic.main.activity_main.*
import java.io.*
import java.time.LocalDate
import kotlin.math.round


class MainActivity : AppCompatActivity() {

    @RequiresApi(Build.VERSION_CODES.O)
    private val date: LocalDate = LocalDate.now()
    private val CODE = 1000
    private val filename = "MoonData.txt"
    private val photoManager = PhotoManager()

    private var moonSettings: MoonSettings =
        MoonSettings()


    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        loadData()
        updateView()
    }


    @RequiresApi(Build.VERSION_CODES.O)
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)
        if (requestCode == CODE && resultCode == Activity.RESULT_OK) {
            moonSettings = data?.extras?.get(Utils.Data.toString()) as MoonSettings
            saveData()
        }
        updateView()
    }

    fun fullMoonListener(view: View) {
        val intent = Intent(this, FullMoonActivity::class.java)
        intent.putExtra(Utils.Data.toString(), moonSettings)
        startActivityForResult(intent, CODE)
    }

    fun settingsListener(view: View) {
        val intent = Intent(this, SettingsActivity::class.java)
        intent.putExtra(Utils.Data.toString(), moonSettings)
        startActivityForResult(intent, CODE)
    }

    private fun saveData() {
        val file = File(this.getExternalFilesDir(null), filename)
        try {
            ObjectOutputStream(FileOutputStream(file)).use { it.writeObject(moonSettings) }
            Toast.makeText(this, "Changes saved", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error occurred during saving!", Toast.LENGTH_SHORT).show()
        }

    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun loadData() {
        try {
            val file = File(this.getExternalFilesDir(null), filename)
            if (file.exists()) {
                ObjectInputStream(FileInputStream(file)).use {
                    moonSettings = it.readObject() as MoonSettings
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Error occurred during loading!", Toast.LENGTH_SHORT).show()
        }
    }

    @RequiresApi(Build.VERSION_CODES.O)
    private fun updateView() {
        val result =
            moonSettings.algorithm.calculate(date)
        val phasePercent = round(result / 29 * 10000) / 100
        val lastNewDate: LocalDate = date.minusDays(result.toLong())
        val nextFullDate = if (result <= 15) {
            date.plusDays(15 - result.toLong())
        } else {
            date.plusDays(30 - result.toLong() + 15)
        }

        today.text = "Lunar phase today: $phasePercent%"
        lastNewMoon.text = "Last new moon was: $lastNewDate"
        nextFullMoon.text = "Next full moon will be: $nextFullDate"
        moonImage.setImageResource(photoManager.receivePhotoId(result, moonSettings.isNorthSide))
    }

}
