package com.senpro.firststep

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class MessageDbHelper(context: Context) :
    SQLiteOpenHelper(context, DATABASE_NAME, null, DATABASE_VERSION) {

    companion object {
        const val DATABASE_NAME = "messages.db"
        const val DATABASE_VERSION = 1
        const val TABLE_NAME = "messages"
        const val COLUMN_ID = "_id"
        const val COLUMN_TEXT = "text"
        const val COLUMN_IS_USER = "is_user"
    }

    override fun onCreate(db: SQLiteDatabase) {
        val createTableQuery = "CREATE TABLE $TABLE_NAME (" +
                "$COLUMN_ID INTEGER PRIMARY KEY AUTOINCREMENT," +
                "$COLUMN_TEXT TEXT NOT NULL," +
                "$COLUMN_IS_USER INTEGER NOT NULL)"
        db.execSQL(createTableQuery)
    }

    override fun onUpgrade(db: SQLiteDatabase, oldVersion: Int, newVersion: Int) {
        db.execSQL("DROP TABLE IF EXISTS $TABLE_NAME")
        onCreate(db)
    }

    fun addMessage(message: Message) {
        val db = writableDatabase
        val values = ContentValues().apply {
            put(COLUMN_TEXT, message.text)
            put(COLUMN_IS_USER, if (message.isUser) 1 else 0)
        }
        db.insert(TABLE_NAME, null, values)
        db.close()
    }

    fun getMessages(): List<Message> {
        val messages = mutableListOf<Message>()
        val db = readableDatabase
        val cursor = db.rawQuery("SELECT * FROM $TABLE_NAME", null)
        while (cursor.moveToNext()) {
            val text = cursor.getString(cursor.getColumnIndexOrThrow(COLUMN_TEXT))
            val isUser = cursor.getInt(cursor.getColumnIndexOrThrow(COLUMN_IS_USER)) == 1
            messages.add(Message(text, isUser))
        }
        cursor.close()
        db.close()
        return messages
    }
}