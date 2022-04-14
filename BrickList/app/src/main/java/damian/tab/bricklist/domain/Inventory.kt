package damian.tab.bricklist.domain

import android.database.Cursor
import java.io.Serializable

class Inventory : SQLParser, Serializable {

    var id: Int = -1
    var name: String = ""
    var active: Int = 1
    var lastAccess: Int = 0

    constructor()
    constructor(id: Int, name: String, active: Int, date: Int) {
        this.id = id
        this.name = name
        this.active = active
        this.lastAccess = date
    }


    override fun parse(cursor: Cursor): Inventory {
        id = cursor.getInt(0)
        name = cursor.getString(1)
        active = cursor.getInt(2)
        lastAccess = cursor.getInt(3)
        return this
    }

}