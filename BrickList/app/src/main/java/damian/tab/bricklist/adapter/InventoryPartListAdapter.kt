package damian.tab.bricklist.adapter

import android.annotation.SuppressLint
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.BitmapDrawable
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.Button
import android.widget.ImageView
import android.widget.TextView
import com.squareup.picasso.Picasso
import damian.tab.bricklist.IMAGE_URL_1
import damian.tab.bricklist.IMAGE_URL_2
import damian.tab.bricklist.IMAGE_URL_3
import damian.tab.bricklist.R
import damian.tab.bricklist.database.SQLExecutor
import damian.tab.bricklist.domain.InventoryPart
import damian.tab.bricklist.task.DownloadImageAsyncTask

class InventoryPartListAdapter(
    context: Context,
    private val inventoryParts: List<InventoryPart>
) : BaseAdapter() {

    private var inflater: LayoutInflater =
        context.getSystemService(Context.LAYOUT_INFLATER_SERVICE) as LayoutInflater

    override fun getCount(): Int {
        return inventoryParts.size
    }

    override fun getItem(position: Int): InventoryPart {
        return inventoryParts[position]
    }

    override fun getItemId(position: Int): Long {
        return position.toLong()
    }

    @SuppressLint("ViewHolder", "SetTextI18n")
    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val rowView = inflater.inflate(R.layout.inventory_part, parent, false)
        val nameTextView = rowView.findViewById(R.id.part_name) as TextView
        val quantityTextView = rowView.findViewById(R.id.part_quantity) as TextView
        val imageView = rowView.findViewById(R.id.part_image) as ImageView
        val part = getItem(position)

        nameTextView.text = part.name + " [" + part.itemCode + "]\n\n" + part.color
        quantityTextView.text = generateQuantityText(part)

        if (part.image == null) {
            loadLazyImages(part, imageView)
        } else if (imageView.drawable == null) {
            imageView.setImageBitmap(part.image)
        }

        rowView.findViewById<Button>(R.id.plus_button).setOnClickListener {
            changeQuantity(part, quantityTextView, rowView, position, 1)
        }
        rowView.findViewById<Button>(R.id.minus_button).setOnClickListener {
            changeQuantity(part, quantityTextView,  rowView, position, -1)
        }
        changeRowColor(part, rowView)
        return rowView
    }

    private fun loadLazyImages(part: InventoryPart, imageView: ImageView) {
        Picasso.get().load(IMAGE_URL_1 + part.designCode.toString())
            .into(imageView, object : com.squareup.picasso.Callback {
                override fun onSuccess() {
                    part.image = (imageView.drawable as BitmapDrawable).bitmap
                    SQLExecutor.updateImageInBLOB(part)
                }

                override fun onError(e: java.lang.Exception?) {
                    val url =
                        if (part.colorCode == null || part.colorCode == 0) IMAGE_URL_2 + part.itemCode + ".jpg"
                        else IMAGE_URL_3 + part.colorCode + "/" + part.itemCode + ".jpg"

                    Picasso.get().load(url).into(imageView, object : com.squareup.picasso.Callback {
                        override fun onSuccess() {
//                            No design code so we can't save in database
                            part.image = (imageView.drawable as BitmapDrawable).bitmap
                        }

                        override fun onError(e: java.lang.Exception?) {
                            val imageTask = DownloadImageAsyncTask(part, imageView)
                            imageTask.execute()
                        }
                    })
                }
            })
    }

    private fun changeQuantity(
        inventoryPart: InventoryPart,
        quantityTextView: TextView,
        view: View,
        position: Int,
        valueToAdd: Int
    ) {
        inventoryPart.quantityInStore += valueToAdd
        if (inventoryPart.quantityInStore < 0 || inventoryPart.quantityInStore > inventoryPart.quantityInSet) {
            inventoryPart.quantityInStore -= valueToAdd
        } else {
            inventoryParts[position].quantityInStore = inventoryPart.quantityInStore
            quantityTextView.text = generateQuantityText(inventoryPart)
            changeRowColor(inventoryPart, view)
        }
    }

    private fun changeRowColor(inventoryPart: InventoryPart, view: View) {
        if (inventoryPart.quantityInSet > inventoryPart.quantityInStore) {
            view.setBackgroundColor(Color.WHITE)
        } else {
            view.setBackgroundColor(Color.LTGRAY)
        }
    }

    private fun generateQuantityText(inventoryPart: InventoryPart): String {
        return (inventoryPart.quantityInStore).toString() + " of " + inventoryPart.quantityInSet.toString()
    }
}