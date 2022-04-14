package damian.tab.bricklist

import android.content.Context
import android.content.SharedPreferences
import damian.tab.bricklist.domain.SQLParser

// Main
const val REQUEST_CODE = 1000

// Settings
const val SETTINGS_NAME = "brickList_settings_data"
const val SETTINGS_MODE = Context.MODE_PRIVATE
const val DATABASE_URL_FIELD = "database_url"
const val DATABASE_VERSION_FIELD = "database_versions"
const val SHOW_ARCHIVED_FIELD = "show_archived"

//Default value
const val DEFAULT_ARCHIVED_VALUE = false
const val DEFAULT_DATABASE_URL = "http://fcds.cs.put.poznan.pl/MyWeb/BL/"

// Database
const val ASSETS_PATH = "databases"
const val DATABASE_NAME = "BrickList.db"
const val DATABASE_VERSION = 1

//Intent data
const val INVENTORY_DATA = "inventory_data"

//Image URLs
const val IMAGE_URL_1 = "https://www.lego.com/service/bricks/5/2/"
const val IMAGE_URL_2 = "https://www.bricklink.com/PL/"
const val IMAGE_URL_3 = "http://img.bricklink.com/P/"


inline fun SharedPreferences.apply(action: SharedPreferences.Editor.() -> Unit) {
    val editor = this.edit()
    action.invoke(editor)
    editor.apply()
}

fun getTodayDate(): Int {
    return (System.currentTimeMillis() / 1000).toInt()
}

open class Factory<T : SQLParser>(private val type: Class<T>) {
    val name: String
        get() = type.name

    fun newInstance(): T = type.newInstance()
}