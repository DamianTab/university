package damian.tab.bricklist.domain

import android.database.Cursor

interface SQLParser {
    fun parse(cursor: Cursor): SQLParser
}