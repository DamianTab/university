package damian.tab.bricklist.database

import android.content.Context
import android.content.SharedPreferences
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import damian.tab.bricklist.*
import java.io.File
import java.io.FileOutputStream

class DatabaseManager(private val context: Context) :
    SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    private val sharedPreferences: SharedPreferences =
        context.getSharedPreferences(SETTINGS_NAME, SETTINGS_MODE)

    override fun onCreate(db: SQLiteDatabase?) {
    }

    override fun onUpgrade(db: SQLiteDatabase?, oldVersion: Int, newVersion: Int) {
    }

    override fun getReadableDatabase(): SQLiteDatabase {
        installOrUpdateIfNecessary()
        return super.getReadableDatabase()
    }

    private fun installOrUpdateIfNecessary() {
        if (isDatabaseOutdated()) {
            context.deleteDatabase(DATABASE_NAME)
            installDatabaseFromAssets()
            sharedPreferences.apply { putInt(DATABASE_VERSION_FIELD, DATABASE_VERSION) }
        }
    }

    private fun installDatabaseFromAssets() {
        val inputStream = context.assets.open("$ASSETS_PATH/$DATABASE_NAME")
        try {
            val outputFile = File(context.getDatabasePath(DATABASE_NAME).path)
            FileOutputStream(outputFile).use {
                inputStream.copyTo(it)
                inputStream.close()
                it.flush()
            }
        } catch (exception: Throwable) {
            throw RuntimeException("The $DATABASE_NAME database couldn't be installed.", exception)
        }
    }


    private fun isDatabaseOutdated(): Boolean {
        return sharedPreferences.getInt(DATABASE_VERSION_FIELD, 0) < DATABASE_VERSION
    }
}