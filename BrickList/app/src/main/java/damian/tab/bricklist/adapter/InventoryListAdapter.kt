package damian.tab.bricklist.adapter

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.graphics.Color
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.TextView
import damian.tab.bricklist.INVENTORY_DATA
import damian.tab.bricklist.InventoryPropertiesActivity
import damian.tab.bricklist.MainActivity
import damian.tab.bricklist.REQUEST_CODE
import damian.tab.bricklist.domain.Inventory

class InventoryListAdapter(
    private val context: Context,
    private val inventories: List<Inventory>
) : BaseAdapter() {

    private var inflater: LayoutInflater =
        context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

    override fun getCount(): Int {
        return inventories.size
    }

    override fun getItem(position: Int): Inventory {
        return inventories[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    @SuppressLint("ViewHolder")
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val rowView = inflater.inflate(android.R.layout.simple_list_item_1, parent, false)
        val nameTextView = rowView.findViewById(android.R.id.text1) as TextView
        val inventory = getItem(position)

        if (inventory.active == 0) {
            nameTextView.setTextColor(Color.LTGRAY)
            nameTextView.text = inventory.name + " (Archvied)"
        } else {
            nameTextView.text = inventory.name
        }

        nameTextView.setOnClickListener {
            val selectedInventory = this.inventories[position]
            val intent = Intent(context, InventoryPropertiesActivity::class.java)
            intent.putExtra(INVENTORY_DATA, selectedInventory)
            (context as MainActivity).startActivityForResult(intent, REQUEST_CODE)
        }
        return rowView
    }
}