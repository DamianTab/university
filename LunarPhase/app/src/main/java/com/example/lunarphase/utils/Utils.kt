package com.example.lunarphase.utils

enum class Utils {
    Data("data");

    private val dataName: String

    constructor(dataName: String) {
        this.dataName = dataName
    }

    override fun toString(): String {
        return dataName
    }


}