package damian.tab.bricklist

import android.app.Activity
import android.content.SharedPreferences
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_settings.*

class SettingsActivity : AppCompatActivity() {

    private lateinit var sharedPreferences: SharedPreferences

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)
        sharedPreferences = getSharedPreferences(SETTINGS_NAME, SETTINGS_MODE)
        url_input.setText(sharedPreferences.getString(DATABASE_URL_FIELD, DEFAULT_DATABASE_URL))
        archived_switch.isChecked =
            sharedPreferences.getBoolean(SHOW_ARCHIVED_FIELD, DEFAULT_ARCHIVED_VALUE)
    }

    override fun finish() {
        sharedPreferences.apply { putString(DATABASE_URL_FIELD, url_input.text.toString()) }
        sharedPreferences.apply { putBoolean(SHOW_ARCHIVED_FIELD, archived_switch.isChecked) }
        setResult(Activity.RESULT_OK, intent)
        Toast.makeText(this, "Settings saved !", Toast.LENGTH_SHORT).show()
        super.finish()
    }
}
