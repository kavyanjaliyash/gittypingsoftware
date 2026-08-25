"""
LMS Production Seeding System.
Contains seed data exported from local SQLite database (courses, lessons, lesson_screens, typing_games).
Preserves exact primary keys and foreign key relationships.
"""

import sys
from database import db
from models import Course, Lesson, Screen, TypingGame

COURSES_DATA = [
    {
        "course_id": 1,
        "course_name": "English Typing",
        "status": "Active"
    },
    {
        "course_id": 2,
        "course_name": "Kannada Typing",
        "status": "Active"
    }
]

LESSONS_DATA = [
    {
        "lesson_id": 1,
        "course_id": 1,
        "lesson_title": "J,F and Space",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 2,
        "course_id": 1,
        "lesson_title": "U, R, and K Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 3,
        "course_id": 1,
        "lesson_title": "D, E, and I Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 4,
        "course_id": 2,
        "lesson_title": "\u0cb8\u0ccd\u0cb5\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 5,
        "course_id": 1,
        "lesson_title": "C, G, and N Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 7,
        "course_id": 1,
        "lesson_title": "T, S, and L Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 5,
        "status": "Active"
    },
    {
        "lesson_id": 8,
        "course_id": 1,
        "lesson_title": "O, B, and A Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 6,
        "status": "Active"
    },
    {
        "lesson_id": 9,
        "course_id": 1,
        "lesson_title": "V, H, and M Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 7,
        "status": "Active"
    },
    {
        "lesson_id": 10,
        "course_id": 1,
        "lesson_title": "Common English Words",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 11,
        "course_id": 1,
        "lesson_title": "Easy Home Row Words",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 12,
        "course_id": 1,
        "lesson_title": "Easy Top Row Words",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 13,
        "course_id": 1,
        "lesson_title": " Period and Comma",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 8,
        "status": "Active"
    },
    {
        "lesson_id": 14,
        "course_id": 1,
        "lesson_title": "W, X, and ; Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 9,
        "status": "Active"
    },
    {
        "lesson_id": 15,
        "course_id": 1,
        "lesson_title": " Q, Y, and P Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 10,
        "status": "Active"
    },
    {
        "lesson_id": 16,
        "course_id": 1,
        "lesson_title": "Z and Enter Keys",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 11,
        "status": "Active"
    },
    {
        "lesson_id": 17,
        "course_id": 1,
        "lesson_title": "Easy Bottom Row Words",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 18,
        "course_id": 1,
        "lesson_title": "Shift Key and Capitalization",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 5,
        "status": "Active"
    },
    {
        "lesson_id": 19,
        "course_id": 1,
        "lesson_title": "Basic Punctuation",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 6,
        "status": "Active"
    },
    {
        "lesson_id": 20,
        "course_id": 1,
        "lesson_title": " Intermediate Punctuation",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 7,
        "status": "Active"
    },
    {
        "lesson_id": 21,
        "course_id": 1,
        "lesson_title": "Quick Sentences",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 8,
        "status": "Active"
    },
    {
        "lesson_id": 22,
        "course_id": 1,
        "lesson_title": " Short Paragraphs",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 9,
        "status": "Active"
    },
    {
        "lesson_id": 23,
        "course_id": 1,
        "lesson_title": "Speed Drills",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 10,
        "status": "Active"
    },
    {
        "lesson_id": 24,
        "course_id": 1,
        "lesson_title": "Skill Builder",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 25,
        "course_id": 1,
        "lesson_title": "Numbers Letters Numbers",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 26,
        "course_id": 1,
        "lesson_title": "Accuracy Focus",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 27,
        "course_id": 1,
        "lesson_title": "Advanced Symbols",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 28,
        "course_id": 1,
        "lesson_title": "Numbers",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 5,
        "status": "Active"
    },
    {
        "lesson_id": 29,
        "course_id": 2,
        "lesson_title": "\u0c95 \u0cb5\u0cb0\u0ccd\u0c97 (\u0c95 \u0c96 \u0c97 \u0c98 \u0c99)",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 30,
        "course_id": 2,
        "lesson_title": "\u0c9a \u0cb5\u0cb0\u0ccd\u0c97 (\u0c9a \u0c9b \u0c9c \u0c9d \u0c9e)",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 31,
        "course_id": 2,
        "lesson_title": "\u0c9f \u0cb5\u0cb0\u0ccd\u0c97 (\u0c9f \u0ca0 \u0ca1 \u0ca2 \u0ca3)",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 32,
        "course_id": 2,
        "lesson_title": "\u0ca4 \u0cb5\u0cb0\u0ccd\u0c97 (\u0ca4 \u0ca5 \u0ca6 \u0ca7 \u0ca8)",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 5,
        "status": "Active"
    },
    {
        "lesson_id": 33,
        "course_id": 2,
        "lesson_title": "\u0caa \u0cb5\u0cb0\u0ccd\u0c97 (\u0caa \u0cab \u0cac \u0cad \u0cae)",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 6,
        "status": "Active"
    },
    {
        "lesson_id": 34,
        "course_id": 2,
        "lesson_title": "\u0caf \u0cb0\u0cbf\u0c82\u0ca6 \u0c9c\u0ccd\u0c9e \u0cb5\u0cb0\u0cc6\u0c97\u0cc6",
        "lesson_description": "",
        "chapter": "Beginner",
        "display_order": 7,
        "status": "Active"
    },
    {
        "lesson_id": 35,
        "course_id": 2,
        "lesson_title": "\u0c95 \u0cb5\u0cb0\u0ccd\u0c97\u0ca6 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 36,
        "course_id": 2,
        "lesson_title": "\u0c9a \u0cb5\u0cb0\u0ccd\u0c97\u0ca6 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 37,
        "course_id": 2,
        "lesson_title": "\u0c9f \u0cb5\u0cb0\u0ccd\u0c97\u0ca6 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 38,
        "course_id": 2,
        "lesson_title": "\u0ca4 \u0cb5\u0cb0\u0ccd\u0c97\u0ca6 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 39,
        "course_id": 2,
        "lesson_title": "\u0caa \u0cb5\u0cb0\u0ccd\u0c97\u0ca6 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 5,
        "status": "Active"
    },
    {
        "lesson_id": 40,
        "course_id": 2,
        "lesson_title": "\u0c89\u0cb3\u0cbf\u0ca6 \u0cb5\u0ccd\u0caf\u0c82\u0c9c\u0ca8\u0c97\u0cb3 \u0c97\u0cc1\u0ca3\u0cbf\u0ca4\u0cbe\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Intermediate",
        "display_order": 6,
        "status": "Active"
    },
    {
        "lesson_id": 41,
        "course_id": 2,
        "lesson_title": "\u0ca6\u0ccd\u0cb5\u0cbf\u0ca4\u0ccd\u0cb5 \u0c92\u0ca4\u0ccd\u0ca4\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 1,
        "status": "Active"
    },
    {
        "lesson_id": 42,
        "course_id": 2,
        "lesson_title": "\u0cb8\u0c82\u0caf\u0cc1\u0c95\u0ccd\u0ca4 \u0c92\u0ca4\u0ccd\u0ca4\u0c95\u0ccd\u0cb7\u0cb0\u0c97\u0cb3\u0cc1",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 2,
        "status": "Active"
    },
    {
        "lesson_id": 43,
        "course_id": 2,
        "lesson_title": "\u0caa\u0ca6\u0c97\u0cb3 \u0c85\u0cad\u0ccd\u0caf\u0cbe\u0cb8",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 3,
        "status": "Active"
    },
    {
        "lesson_id": 44,
        "course_id": 2,
        "lesson_title": "\u0cb5\u0cbe\u0c95\u0ccd\u0caf\u0c97\u0cb3 \u0c85\u0cad\u0ccd\u0caf\u0cbe\u0cb8",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 4,
        "status": "Active"
    },
    {
        "lesson_id": 45,
        "course_id": 2,
        "lesson_title": "\u0caa\u0ccd\u0caf\u0cbe\u0cb0\u0cbe\u0c97\u0ccd\u0cb0\u0cbe\u0cab\u0ccd\u200c\u0c97\u0cb3 \u0c85\u0cad\u0ccd\u0caf\u0cbe\u0cb8 (Paragraph)",
        "lesson_description": "",
        "chapter": "Advanced",
        "display_order": 5,
        "status": "Active"
    }
]

SCREENS_DATA = [
    {
        "screen_id": 1,
        "lesson_id": 1,
        "screen_title": "Screen 1",
        "screen_content": "jjjjjjjj",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 2,
        "lesson_id": 1,
        "screen_title": "Screen 2",
        "screen_content": "fffjfffjfffjfffjffffjjjjfjfjfjfjf",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 3,
        "lesson_id": 4,
        "screen_title": "1",
        "screen_content": "\u0c85\u0c85\u0c85\u0c85\u0c85\u0c85\u0c85\u0c85\r\n\u0c86\u0c86\u0c86\u0c86\u0c86\u0c86\u0c86\u0c86\r\n\u0c87\u0c87\u0c87\u0c87\u0c87\u0c87\u0c87\u0c87\r\n\u0c88\u0c88\u0c88\u0c88\u0c88\u0c88\u0c88\u0c88\r\n\u0c89\u0c89\u0c89\u0c89\u0c89\u0c89\u0c89\u0c89\r\n\u0c8a\u0c8a\u0c8a\u0c8a\u0c8a\u0c8a\u0c8a\u0c8a\r\n\u0c8b\u0c8b\u0c8b\u0c8b\u0c8b\u0c8b\u0c8b\u0c8b\r\n\u0c8e\u0c8e\u0c8e\u0c8e\u0c8e\u0c8e\u0c8e\u0c8e\r\n\u0c8f\u0c8f\u0c8f\u0c8f\u0c8f\u0c8f\u0c8f\u0c8f\r\n\u0c90\u0c90\u0c90\u0c90\u0c90\u0c90\u0c90\u0c90\r\n\u0c92\u0c92\u0c92\u0c92\u0c92\u0c92\u0c92\u0c92\r\n\u0c93\u0c93\u0c93\u0c93\u0c93\u0c93\u0c93\u0c93\r\n\u0c94\u0c94\u0c94\u0c94\u0c94\u0c94\u0c94\u0c94\r\n\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\u0c85\u0c82\r\n\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83\u0c85\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 4,
        "lesson_id": 4,
        "screen_title": "2",
        "screen_content": "\u0c85\u0c86\u0c85\u0c86\u0c85\u0c86\u0c85\u0c86\r\n\u0c87\u0c88\u0c87\u0c88\u0c87\u0c88\u0c87\u0c88\r\n\u0c89\u0c8a\u0c89\u0c8a\u0c89\u0c8a\u0c89\u0c8a\r\n\u0c8b\u0c8e\u0c8b\u0c8e\u0c8b\u0c8e\u0c8b\u0c8e\r\n\u0c8f\u0c90\u0c8f\u0c90\u0c8f\u0c90\u0c8f\u0c90\r\n\u0c92\u0c93\u0c92\u0c93\u0c92\u0c93\u0c92\u0c93\r\n\u0c94\u0c85\u0c82\u0c94\u0c85\u0c82\u0c94\u0c85\u0c82\u0c94\u0c85\u0c82\r\n\u0c85\u0c83\u0c85\u0c85\u0c83\u0c85\u0c85\u0c83\u0c85\u0c85\u0c83\u0c85\u0c83",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 5,
        "lesson_id": 1,
        "screen_title": "Screen 3",
        "screen_content": "jjfffjjjfffjjjjffffjfjfjjffj",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 6,
        "lesson_id": 1,
        "screen_title": "Screen 4",
        "screen_content": "fffjjjfffjjjffjjfffjfjfjjjfjfjffj",
        "screen_type": "jump",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 7,
        "lesson_id": 1,
        "screen_title": "Screen5",
        "screen_content": " j j j j j j j j j j",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 8,
        "lesson_id": 1,
        "screen_title": "Screen 6",
        "screen_content": "jjfjff ffjfjj\r\njffjf jfjf\r\nffjffj ffjjjffj\r\nfjfjfjfj",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 9,
        "lesson_id": 2,
        "screen_title": "Screen1",
        "screen_content": "uuujuuujuuujuuujuj uu ju",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 10,
        "lesson_id": 2,
        "screen_title": "Screen2",
        "screen_content": "rrrfrrrfrrfrrfrrf rr fr",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 11,
        "lesson_id": 2,
        "screen_title": "Screen3",
        "screen_content": "uurrrruruururruuurururrruuurrru",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 13,
        "lesson_id": 2,
        "screen_title": "Screen4",
        "screen_content": "kkkkkkkkkjjjkkjjkkjj",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 14,
        "lesson_id": 2,
        "screen_title": "Screen5",
        "screen_content": "jjjkjjkjjkkjkjrrrjkkfrffrrkjjkkrjjfffrrkkrrjfkr",
        "screen_type": "jump",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 15,
        "lesson_id": 2,
        "screen_title": "Screen6",
        "screen_content": "kkkk uuuu rrrr uuuu\r\nk kkk rrrr uuuu kkkk\r\nuuuu rrrr rr uu kk",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 16,
        "lesson_id": 2,
        "screen_title": "Screen7",
        "screen_content": "kuf ruk kur ruf fur kurf kuf rukk kur ruff",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 17,
        "lesson_id": 2,
        "screen_title": "Screen8",
        "screen_content": "ruff fur ruff fur k ruff furr\r\nfur ruff k ruff furr ruff fur",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 18,
        "lesson_id": 3,
        "screen_title": "Screen1",
        "screen_content": "ddddffffddddffffdffdffdd",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 19,
        "lesson_id": 3,
        "screen_title": "Screen2",
        "screen_content": "iiiikkkkiiiikkkkikkikkii",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 20,
        "lesson_id": 3,
        "screen_title": "Screen3",
        "screen_content": "ddiidddiiiddiidididiiidiididididiiiiddddii",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 21,
        "lesson_id": 3,
        "screen_title": "Screen4",
        "screen_content": "eeeeddddeeeeddddeeddeeddeeffeedd",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 22,
        "lesson_id": 3,
        "screen_title": "Screen5",
        "screen_content": "eeeddddiiiikkkkeeiiieiiiieeeeieieieiei",
        "screen_type": "waterfall",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 23,
        "lesson_id": 3,
        "screen_title": "Screen6",
        "screen_content": "dddddeeeddddeeekkkikkkikkkikkkidekidekidddekkkidekideddkikkdeddkikk",
        "screen_type": "jump",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 24,
        "lesson_id": 3,
        "screen_title": "Screen7",
        "screen_content": "jid kid rid eid jid kid rid eid\r\nkirk kird kirf k ire kid r fied",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 25,
        "lesson_id": 3,
        "screen_title": "Screen8",
        "screen_content": "fred did kik red fire fed duke\r\nkirk fed fred fur fire if red kk",
        "screen_type": "block",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 26,
        "lesson_id": 3,
        "screen_title": "Screen9",
        "screen_content": "dire\r\ndue\r\nduke\r\nred\r\nfeud\r\nfir\r\nfire\r\nfeud\r\nfir\r\nfire\r\nfired\r\nfur\r\nid\r\nif\r\nire\r\njurk\r\nred\r\nref\r\nrid\r\nride\r\nrife\r\nrude\r\n\r\n\r\n",
        "screen_type": "jump",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 27,
        "lesson_id": 3,
        "screen_title": "Screen10",
        "screen_content": "fire jure feud juke jedi fuji\r\nrudie fried fired irked fired\r\njerid juked duiker juried dire",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 28,
        "lesson_id": 5,
        "screen_title": "Screen1",
        "screen_content": "cdcdccddccddccddccccddcc",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 29,
        "lesson_id": 5,
        "screen_title": "Screen2",
        "screen_content": "njnjnjnjnnjjnnjnnjnjjnnnnjjjj",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 30,
        "lesson_id": 5,
        "screen_title": "Screen3",
        "screen_content": "ccnnnnccnnncnncnnncccnnnncnncnnncnccncnccncccncnccn",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 31,
        "lesson_id": 5,
        "screen_title": "Screen4",
        "screen_content": "dcc jnndcc jnnccd nnjdcc jnnjdcnncjdncjdncjd",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 32,
        "lesson_id": 5,
        "screen_title": "Screen5",
        "screen_content": "cdc\r\nnjn\r\ncnn\r\nc\r\nn\r\nn\r\nncc\r\nncc\r\ndc\r\nn\r\nc\r\nc",
        "screen_type": "jump",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 33,
        "lesson_id": 5,
        "screen_title": "Screen6",
        "screen_content": "gfgfgfgfggffggffggggffff",
        "screen_type": "block",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 34,
        "lesson_id": 5,
        "screen_title": "Screen7",
        "screen_content": "nnjjggggnnngnngnggnnnjjjgggfffnnngnfgnjgnn",
        "screen_type": "waterfall",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 35,
        "lesson_id": 5,
        "screen_title": "Screen8",
        "screen_content": "f gg j nn g gg nnn\r\nfnf j gj f gg jnn\r\nggn n ng fgfg\r\njnjn ngng fgfg",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 36,
        "lesson_id": 5,
        "screen_title": "Screen9",
        "screen_content": "cure end diner cider end\r\ncued dice induce deduce\r\nCid duck dine ice iced",
        "screen_type": "paragraph",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 44,
        "lesson_id": 7,
        "screen_title": "Screen1",
        "screen_content": "tttttttffffttttffttfftt",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 45,
        "lesson_id": 7,
        "screen_title": "Screen2",
        "screen_content": "lllllllkkkkllllllkkllkk",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 46,
        "lesson_id": 7,
        "screen_title": "Screen3",
        "screen_content": "ttlltltltttttllllttffllkkllkkttffttff",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 47,
        "lesson_id": 7,
        "screen_title": "Screen4",
        "screen_content": "f ttt ff ttt fttf lll k ll ft kl ft ffttkkll",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 48,
        "lesson_id": 7,
        "screen_title": "Screen5",
        "screen_content": "sssssssddddsssssdsdsdsdsdfsdfsdf",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 49,
        "lesson_id": 7,
        "screen_title": "Screen6",
        "screen_content": "sslllslslsslsllslslllslssllllsssllsslslsl",
        "screen_type": "waterfall",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 50,
        "lesson_id": 7,
        "screen_title": "Screen7",
        "screen_content": "tsltlslstllslsslsttttllssstsltltttlssltltslsssttll",
        "screen_type": "waterfall",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 51,
        "lesson_id": 7,
        "screen_title": "Screen8",
        "screen_content": "es\r\net\r\nis\r\nit\r\nli\r\nsi\r\nst\r\nte\r\nti\r\nus\r\nut\r\nlie\r\nlis\r\nlit\r\nsei\r\nsel\r\nset\r\nsue\r\nsui\r\ntel\r\ntes\r\ntie\r\ntil\r\nsit",
        "screen_type": "block",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 52,
        "lesson_id": 7,
        "screen_title": "Screen9",
        "screen_content": "slug ties tile silt lute lets stile\r\nnicest signed tunic uncles genius\r\nkings signet single suited united\r\nluces diner cutie glens list guile",
        "screen_type": "paragraph",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 53,
        "lesson_id": 7,
        "screen_title": "Screen10",
        "screen_content": "trucking clinkers stickler\r\ninjured funkier side stick\r\ngifted gunk trunk linger",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 54,
        "lesson_id": 8,
        "screen_title": "Screen1",
        "screen_content": "ooooooolllloooolloolloo",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 55,
        "lesson_id": 8,
        "screen_title": "Screen2",
        "screen_content": "bbbbbbbffffbbbbffbbffbb",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 56,
        "lesson_id": 8,
        "screen_title": "Screen3",
        "screen_content": "bbbbfffooolllbbbffffolbbobbbobbbffggbboollkkgbgfolkolk",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 57,
        "lesson_id": 8,
        "screen_title": "Screen4",
        "screen_content": "loo\r\nfbb\r\nloo\r\nfbb\r\nool\r\nbbf\r\nloo\r\nfbb\r\nflob\r\nbofl\r\nbofl\r\nbofl\r\nflob",
        "screen_type": "jump",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 58,
        "lesson_id": 8,
        "screen_title": "Screen5",
        "screen_content": "obb obb o b b boo boo b o o obo bob\r\nbob obo o o b boo boo b b o obb boo",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 59,
        "lesson_id": 8,
        "screen_title": "Screen6",
        "screen_content": "aaaaassssaaaasasasa",
        "screen_type": "block",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 60,
        "lesson_id": 8,
        "screen_title": "Screen7",
        "screen_content": "bbaaaabbbabbabbabaabbbbababab",
        "screen_type": "waterfall",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 61,
        "lesson_id": 8,
        "screen_title": "Screen8",
        "screen_content": "ob bo ba ab ba bo ob abobo a oba ab",
        "screen_type": "block",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 62,
        "lesson_id": 8,
        "screen_title": "Screen9",
        "screen_content": "tab sob sat oat lot lob lab\r\ntabs slot slob slab salt lost\r\ngnats globs gloat bolts boats\r\nboast blots blogs bloat blats\r\nblast baton angst altos along",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 63,
        "lesson_id": 8,
        "screen_title": "Screen10",
        "screen_content": "abides adobes bailed bard\r\nconed conga dance design\r\n\r\ndingo genic incog ocean\r\nceding canoed cabbage\r\nbeading decagon coinage",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 64,
        "lesson_id": 9,
        "screen_title": "Screen1",
        "screen_content": "vvvvvvvffffvvvvffvvffvv",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 65,
        "lesson_id": 10,
        "screen_title": "Screen1",
        "screen_content": "the of to and a in is it you that he\r\nwas for on are with as i his they be at one have\r\nthis from or had by hot but some what there we\r\ncan out other were all your when up use word\r\nhow said an each she which do their time if will\r\nway about",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 66,
        "lesson_id": 10,
        "screen_title": "Screen2",
        "screen_content": "many then them would write like so\r\nthese her long \r\nmake thing see him two has look more\r\nday could go\r\ncome did my sound no most number who\r\nover know\r\nwater than call first people may down\r\nside been\r\nnow find any new work part take get\r\nplace made",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 67,
        "lesson_id": 10,
        "screen_title": "Screen3",
        "screen_content": "live where after back little only round\r\nman year\r\ncame show every good me give our under\r\nname very\r\nthrough just form much great think say\r\nhelp low\r\nline before turn cause same mean differ\r\nmove right\r\nboy old too does tell sentence set\r\nthree want air",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 68,
        "lesson_id": 11,
        "screen_title": "Scren1",
        "screen_content": "add all alley aft agh ask afford ajar\r\nadapt arf ate art app arty awe aww apt\r\narr aught apt award abs acct among\r\naztec ant am avenue acorn axe ach",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 69,
        "lesson_id": 11,
        "screen_title": "Screen2",
        "screen_content": "salad slap slide shell sad sat shall\r\nshad Shaq super sure sip sod side sewer\r\nsell soup sire sue sam sack salmon\r\nsniper snack snoop",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 70,
        "lesson_id": 11,
        "screen_title": "Screen3",
        "screen_content": "dad dan decide dag darpa dart defer\r\ndeter dash dip destiny dread dew do\r\ndipity dud did dui dirt d ax dimmer\r\ndinner dav dam d ax dent doom dabble",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 71,
        "lesson_id": 11,
        "screen_title": "Screen4",
        "screen_content": "fan flirt fact flute flapper fill fed\r\nfun few fewer fist fern fanatic fancy\r\nfab fennel fervor",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 72,
        "lesson_id": 11,
        "screen_title": "Screen5",
        "screen_content": "gandalf garden gas gad gallant gapless\r\ngallery great goo good gin guard garden\r\ngreen gwen gamma gammy gym gabby gib\r\ngone g aven",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 73,
        "lesson_id": 11,
        "screen_title": "Screen6",
        "screen_content": "has hat half haha ham halpert had handy\r\nhelmet hep hurting hip heart hem hurt\r\nhew hippo heard hand hammy hen hummer\r\nhunger hack hax hammer hung",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 74,
        "lesson_id": 11,
        "screen_title": "Screen7",
        "screen_content": "jason jam jan jail jandy jag jandy jalp\r\njaff jas jest jen jill john joyous\r\njimmy joomla jester jim jam jabber\r\njamming j ax jav vy jammers jandy jazz",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 75,
        "lesson_id": 11,
        "screen_title": "Screen8",
        "screen_content": "kayak kernite keystroke kiddy key\r\nkitten kelp keyboard king kite knot\r\nkarma knife knee kemp kick",
        "screen_type": "block",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 76,
        "lesson_id": 11,
        "screen_title": "Screen9",
        "screen_content": "lamb ladybug last lamp lad laugh lard\r\nloss leaf lollipop lips log lion lemon\r\nloud 100 lack Iamb lam lob labs lament\r\nlavish",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 77,
        "lesson_id": 13,
        "screen_title": "Screen1",
        "screen_content": ",,,,,,,kkkk,,,,kk,,kk,,",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 78,
        "lesson_id": 13,
        "screen_title": "Screen2",
        "screen_content": ".......llll....ll..ll..",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 79,
        "lesson_id": 13,
        "screen_title": "Screen3",
        "screen_content": ",,,,kkkk....llll,,kl.,kl.,kl.,klkll..,,",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 80,
        "lesson_id": 13,
        "screen_title": "Screen4",
        "screen_content": "l.k,l..k,,..l,,k.l,k,,..,. ,. .,",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 81,
        "lesson_id": 13,
        "screen_title": "Screen5",
        "screen_content": "l.k.j.h.g.f.d.s.f.g.h.j.k.l.u.r.i.e.r.t.u.m.",
        "screen_type": "waterfall",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 82,
        "lesson_id": 13,
        "screen_title": "Screen6",
        "screen_content": "j.\r\nk.\r\nl.\r\nu.\r\ni.\r\no.\r\nm.\r\nn.\r\nh.\r\ng.\r\nf,\r\nd,\r\ns,\r\na,\r\nt,\r\nr,\r\ne,\r\nb,\r\nv,\r\nc,",
        "screen_type": "jump",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 83,
        "lesson_id": 13,
        "screen_title": "Screen7",
        "screen_content": "job. ham. hob. jab, jam, mob, ohm. ova,\r\nfoam. jamb, lamb. lash,\r\nlast. lath, loath. lobs.",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 84,
        "lesson_id": 13,
        "screen_title": "Screen8",
        "screen_content": "farmfarofoamforkformharmher,him,houryou.him.her,",
        "screen_type": "jump",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 85,
        "lesson_id": 13,
        "screen_title": "Screen9",
        "screen_content": "ovum, raku, roam, abhor, abohm,\r\nsoar, sofa. soft, soma. sorb.\r\nstab, star. stoa, stub. sulk, surf.\r\ntabs, talk. taco, taro. task, thou.\r\nthru, thus. tofu, tomb. talk, tall.",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 86,
        "lesson_id": 14,
        "screen_title": "Screen1",
        "screen_content": "wwwwwwwwsssswwwwsswwssww",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 87,
        "lesson_id": 14,
        "screen_title": "Screen2",
        "screen_content": ";;;;;;;llll;;;;ll;;ll;;",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 88,
        "lesson_id": 14,
        "screen_title": "Screen3",
        "screen_content": "wwss;;llws;lw;;w;www;;;;wwss;;ll;;llsswwssww;;ll",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 89,
        "lesson_id": 14,
        "screen_title": "Screen4",
        "screen_content": "sww l;;;sww l;;ls www sswww l ;;; l ;;; l",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 90,
        "lesson_id": 14,
        "screen_title": "Screen5",
        "screen_content": "xxxxxxxssssxxxxssxxssxx",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 91,
        "lesson_id": 14,
        "screen_title": "Screen6",
        "screen_content": "xxss;;;llxxss;lxs;lxxssww;lxsw;;;lllxxsswwxxssww;;ll;;ll",
        "screen_type": "waterfall",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 92,
        "lesson_id": 14,
        "screen_title": "Screen7",
        "screen_content": "SXS SWS SXS SWS WSX WSX\r\nXSW XSW WSXS XSWS WXWXW\r\nXXXX WWWW XX WW SW SX S",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 93,
        "lesson_id": 14,
        "screen_title": "Screen8",
        "screen_content": "hex how; ho; maw maxx; min; mew; owe\r\nvaw; vex; vow;\r\navow; exam; meow; view;\r\nvoix; wave; wham; whim;",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 94,
        "lesson_id": 14,
        "screen_title": "Screen9",
        "screen_content": "whomwhatwet.whetwho;how;whenwithwax,tax,vex,ox,\r\nmix;",
        "screen_type": "jump",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 95,
        "lesson_id": 14,
        "screen_title": "Screen10",
        "screen_content": "texan. toxic; toxin, twain; vixen.\r\nwaxen; white,\r\nwince, woman; woven. anoxic; unmix,\r\nvarix; wall;\r\nhoax; tax. taxing, texan; tinware,\r\nwrack; wreak; wrecking, wren; wring.",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 96,
        "lesson_id": 15,
        "screen_title": "Screen1",
        "screen_content": "qqqqqqqqaaaaqqqqaaqqaaqq",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 97,
        "lesson_id": 15,
        "screen_title": "Screen2",
        "screen_content": "yyyyyyyjjjjyyyyjjyyjjyy",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 98,
        "lesson_id": 15,
        "screen_title": "Screen3",
        "screen_content": "qqaayjqayyyjjjqqqyyyqqyyy",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 99,
        "lesson_id": 15,
        "screen_title": "Screen4",
        "screen_content": "qqaaqqyyjjyyqayj",
        "screen_type": "waterfall",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 100,
        "lesson_id": 15,
        "screen_title": "Screen5",
        "screen_content": "aqqqjjyyaqqqyjyyyaqqyyjjqayj",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 101,
        "lesson_id": 15,
        "screen_title": "Screen6",
        "screen_content": "ppppppp;;;;pppp;;pp;;pp",
        "screen_type": "block",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 102,
        "lesson_id": 15,
        "screen_title": "Screen7",
        "screen_content": "ppjjjyyypiypphhyyjjhhjjyypp",
        "screen_type": "waterfall",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 103,
        "lesson_id": 15,
        "screen_title": "Screen8",
        "screen_content": "ax ay ex.\r\nox oy we.\r\nwo xi ya;\r\nway wax",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 104,
        "lesson_id": 15,
        "screen_title": "Screen9",
        "screen_content": "wavyyea,painyarnwavyyea,painyarnparepariparkpave",
        "screen_type": "jump",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 105,
        "lesson_id": 15,
        "screen_title": "Screen10",
        "screen_content": "qua quag; quay que.quean, quince, quo, quion;\r\npac pacer, pacing, pack.packer, packing, page.\r\npaw pawing pax paying peaking; pear.pecan perk\r\nyank yap, yarn, yawning yawp.yearn yew yoga yogi\r\nyoking younger your. yuk younger; yank\r\nyag yo. vowing wagon. wakeup vinegar.\r\nvoyage wacky.",
        "screen_type": "block",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 106,
        "lesson_id": 16,
        "screen_title": "Screen1",
        "screen_content": "zzzzzzzzaaaazzzzaazzaazz",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 107,
        "lesson_id": 16,
        "screen_title": "Screen2",
        "screen_content": "\r\n\r\n\r\n\r\n;;;;\r\n\r\n\r\n\r\n;;\r\n\r\n;;\r\n\r\n;\r\n;\r\n;\r\n",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 108,
        "lesson_id": 16,
        "screen_title": "Screen3",
        "screen_content": "zzzaaa\r\n\r\n\r\n;;;zzaa\r\n;zzzaa\r\n\r\n\r\nz\r\nzz\r\n\r\nzzaa\r\n\r\n;;\r\n;\r\n;zaza",
        "screen_type": "waterfall",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 109,
        "lesson_id": 16,
        "screen_title": "Screen4",
        "screen_content": "azzzazzzazzzazzz;;;\r\n\r\n;;\r\n;;;\r\n\r\n;;",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 110,
        "lesson_id": 16,
        "screen_title": "Screen5",
        "screen_content": "zap zep zip quiz\r\nzap zep zip quiz",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 111,
        "lesson_id": 16,
        "screen_title": "Screen6",
        "screen_content": "razerez;ritzrityza\r\nzaz\r\nrazerez;ritzrityza",
        "screen_type": "jump",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 112,
        "lesson_id": 16,
        "screen_title": "Screen7",
        "screen_content": "za zeta zero zit zoa zozzy\r\nwimmy wam wam wozzle",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 113,
        "lesson_id": 16,
        "screen_title": "Screen8",
        "screen_content": "hey, look at that.\r\nyou are an amazing typist.\r\nyou can now type anything.\r\nyou deserve an award.",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 114,
        "lesson_id": 12,
        "screen_title": "Screen1",
        "screen_content": "quartz quail quart quiver queen quilt\r\nquit quack quell qua quadev quest quint\r\nquaint quab",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 115,
        "lesson_id": 12,
        "screen_title": "Screen2",
        "screen_content": "wonder were wet weapon weeds window\r\nwell wonky we wheat when where whack\r\nwander waft wall way waste want waver\r\nwacky wax wave went worn waxing wam",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 116,
        "lesson_id": 12,
        "screen_title": "Screen3",
        "screen_content": "eerie eep eight eyes eel ewe eeple egg elk eagle ear earth eleven earn evil\r\nevangelical even evan extra\r\nrose ring robot record report ruse re rabbit rain rainbow rake rat rhino\r\nraster ram rave recede rummy razzle rabbit",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 117,
        "lesson_id": 12,
        "screen_title": "Screen4",
        "screen_content": "tent tiger toe toilet toad tooth toil tin taxi table tasty tally tattle tail\r\ntan tammy tax taxed tacky tabby\r\nyell yolk yogurt yoyo yelling yippy your yacht yarn yawn yak yam yag y affer\r\nyad yaz y ax yabby y uma young yummy y amax",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 118,
        "lesson_id": 12,
        "screen_title": "Screen5",
        "screen_content": "up upside ur uproot upper son underwhelm usa unicycle understand upstairs\r\numbrella unicorn unhappy uniform uni\r\niris irate ite import i daho iconic icon iguana igloo idea island indigo i lene\r\nice ivy icicle inside important intuit",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 119,
        "lesson_id": 12,
        "screen_title": "Screen6",
        "screen_content": "orange owl or ly ornate orchard ore oar oar odd off offer offering oatmeal ox\r\none oboe oval onto ovate only ox\r\nportly pin pure pods privy pencil pig paint pants pal pail plane plain pan\r\npam pizza pizzas pavel",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 120,
        "lesson_id": 17,
        "screen_title": "Screen1",
        "screen_content": "zigzag zebra zero zipper zinnia zoo zithe zan zala zalad zajar zaddy zamono\r\nzakk zah zomo zanby zabba zamna zaxy zamn\r\nxenops xiphias xerox xenon xylem xerxes x a vier x aks x ader x almo xaghij xalfo xan xemop xenox xemnob xazer xab xzv xamno",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 121,
        "lesson_id": 17,
        "screen_title": "Screen2",
        "screen_content": "cow corn cup cone crony code cola coal cent cen car can camel carrot cake cat \r\ncarp cart card carl cab cabby cammie  candy carny cennel camel candy\r\nvest volcano vote violin vowels vacuum vat van valley velvet vagrant vale vase\r\nvasiform",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 122,
        "lesson_id": 17,
        "screen_title": "Screen3",
        "screen_content": "bee bird broom bus butterfly booths bat balloon bag banana ball ballroom\r\nbavarian banned banner bammy bax\r\nnet nose nest notes nine number nail nair navel nan nap nah nal navigation\r\nnavizon nam nab nax",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 123,
        "lesson_id": 17,
        "screen_title": "Screen4",
        "screen_content": "milk mouse mitten moth mop moon moons\r\nmoop man mask mail mable maple man male\r\nmail monday montel mack mabby maze maps",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 124,
        "lesson_id": 18,
        "screen_title": "1",
        "screen_content": "Jj jj Jj jj Jj jj Jj jj Jj jj\r\nF fff Fff f Fff f F fff F fff\r\njJj jJj j Jj jJj jJj j Jj\r\nf Ff f Ff f Ff f Ff f Ff f Ff",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 125,
        "lesson_id": 18,
        "screen_title": "2",
        "screen_content": "j J fF j J fF kK dD kK dD IL ss hH gG aA\r\nJj Ff Jj Ff Kk Dd Kk Dd LI ss Hh Gg Aa",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 126,
        "lesson_id": 18,
        "screen_title": "3",
        "screen_content": "rR ulJ rR il eE il eE\r\n00 ww 00 ww pp qQ pp qQ\r\nUu Rr I-Ju Rr li Ee li Ee\r\n00 ww 00 ww Pp Qq Pp Qq",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 127,
        "lesson_id": 18,
        "screen_title": "4",
        "screen_content": "mM vv mM vv cc nN cc\r\nnN xx bB xx bB zz zz\r\nMm Vv Mm Vv Cc Nn Cc\r\nNn xx Bb xx Bb zz zz",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 128,
        "lesson_id": 18,
        "screen_title": "5",
        "screen_content": "The Be To Of And A In That Have I It For Not\r\nOn With He As You Do At This But His By From\r\nWould would There there What what into Into\r\nThey are tall.\r\nIt is great.",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 130,
        "lesson_id": 19,
        "screen_title": "1",
        "screen_content": "; '''; ''' ;''' ;'' ;''' ;''' ;''' ;'''''' ''' ;;; '''",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 131,
        "lesson_id": 19,
        "screen_title": "2",
        "screen_content": "won't can't ain't he's he'd it's isn't\r\nshe'd let's",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 132,
        "lesson_id": 19,
        "screen_title": "3",
        "screen_content": "; /// ; /// ; /// ; /// ;/// ;;; //// ; /// ; /// ; /// ; /// /// ;;; /// ;;;",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 133,
        "lesson_id": 19,
        "screen_title": "4",
        "screen_content": "he/she them/us yes/no up/down loud/quiet a/b\r\nwon't/ will can't/ can didn't/ did aren't/ are",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 134,
        "lesson_id": 19,
        "screen_title": "5",
        "screen_content": "Isn't typing with apostrophes great?\r\nBefore this exercise, you couldn't!\r\n\r\nDidn't you know that you can/ will type\r\nfaster? Just spend more time/ effort\r\nevery day, you'll see!",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 135,
        "lesson_id": 19,
        "screen_title": "6",
        "screen_content": "It's fun to type/ keyboard when on your\r\npc/mac; many boys/ girls have found\r\nthat's true.\r\n\r\nWhat do you think/ believe about touch\r\ntyping? I'm pretty sure/ convinced it's\r\nan awesome skill.",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 136,
        "lesson_id": 19,
        "screen_title": "7",
        "screen_content": "It's good she hasn't raced/ run, or\r\nshe'd be very tired. She's got a long\r\nrace/ run ahead of her but you'll see,\r\nshe's going to do great.",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 137,
        "lesson_id": 20,
        "screen_title": "1",
        "screen_content": "; ??? ; ??? ; ; ??? ; ; ??? ; \r\n; ??? ; ??? ; ; ??? ; ; ??? ;\r\n; ??? ; ??? ; ; ??? ; ; ??? ;\r\n; ??? ; ??? ; ; ??? ; ; ??? ;",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 138,
        "lesson_id": 20,
        "screen_title": "2",
        "screen_content": "who? what? where? why? when? how? really?",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 139,
        "lesson_id": 20,
        "screen_title": "3",
        "screen_content": "; \"\"\" ; \"\"\" ; \"\"\" ; \"\"\" ;\r\n; \"\"\" ; \"\"\" ; \"\"\" ; \"\"\" ;\r\n; \"\"\" ; \"\"\" ; \"\"\" ; \"\"\" ;",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 140,
        "lesson_id": 20,
        "screen_title": "4",
        "screen_content": "Hello there.\r\n'Quotes are great.'\r\n\"Talking is fun.",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 141,
        "lesson_id": 20,
        "screen_title": "5",
        "screen_content": "l ::: l ::: l ::: l :::\r\nl ::: l ::: l ::: l :::\r\n::: l ::: l ::: l::: l l l",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 142,
        "lesson_id": 20,
        "screen_title": "6",
        "screen_content": "buy these:\r\nsell those:\r\ntrade these:\r\nwin those:",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 143,
        "lesson_id": 20,
        "screen_title": "7",
        "screen_content": "\"Could you grab that?\"\r\n\"Yes, I can.\"\r\n\"What I feel: thankful.\"",
        "screen_type": "paragraph",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 144,
        "lesson_id": 20,
        "screen_title": "8",
        "screen_content": "Would you call that \"free\"?\r\nWell, what is \"free\"?\r\nFree means: not costing anything.",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 145,
        "lesson_id": 21,
        "screen_title": "1",
        "screen_content": "Whatever you are, be a good one.\r\nBe the change you wish to see in the world.\r\nTry and fail, but never fail to try.",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 146,
        "lesson_id": 21,
        "screen_title": "2",
        "screen_content": "Do one thing every day that scares you.\r\nBelieve you can and you're halfway there.",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 147,
        "lesson_id": 21,
        "screen_title": "3",
        "screen_content": "Let your memory be your travel bag.\r\nTo travel is to take a journey into yourself.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 148,
        "lesson_id": 21,
        "screen_title": "4",
        "screen_content": "I haven't been everywhere, but it's on my list.\r\nIf you come to a fork in the road, take it.\r\n",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 149,
        "lesson_id": 21,
        "screen_title": "5",
        "screen_content": "April has put a spirit of youth in everything.",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 150,
        "lesson_id": 22,
        "screen_title": "1",
        "screen_content": "Tracy looked at the flag. The flag is\r\nred, white, and blue. It has fifty\r\nwhite stars, seven red stripes, and six\r\nwhite stripes.",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 151,
        "lesson_id": 22,
        "screen_title": "2",
        "screen_content": "Donald plays the piano. He loves the\r\npiano. He has a big piano in his living\r\nroom. His piano is shiny and black. It\r\nhas three legs and a bench.",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 152,
        "lesson_id": 22,
        "screen_title": "3",
        "screen_content": "This weekend I went to the zoo. It was\r\ngreat. I went with my mom and dad. My\r\nsister came, too. The zoo was in the\r\ncity. The drive was very long.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 153,
        "lesson_id": 22,
        "screen_title": "4",
        "screen_content": "When I was playing today at recess, I\r\nfelt like a kite blown around by the\r\nwind. It was hard to stay in one place\r\nbecause the wind was so strong.",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 154,
        "lesson_id": 22,
        "screen_title": "5",
        "screen_content": "Do you like apples? I think apples are\r\ngreat. They are a fun fruit to eat.\r\nApples come in many colors, but my\r\nfavorite is green. What is yours?",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 155,
        "lesson_id": 23,
        "screen_title": "1",
        "screen_content": "The quick brown fox jumped over the\r\nlazy dogs.\r\n\r\nA human can live well even in a palace.",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 156,
        "lesson_id": 23,
        "screen_title": "2",
        "screen_content": "True friendship is a plant of slow growth.\r\nI never think of the future;it comes soon enough.\r\n",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 157,
        "lesson_id": 23,
        "screen_title": "3",
        "screen_content": "Eighty percent of life is showing up.\r\nA poem begins in delight and ends in wisdom.\r\nTo drive would be a box of nouns.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 158,
        "lesson_id": 23,
        "screen_title": "4",
        "screen_content": "Long ago I bought a dry gold coin.\r\nThe hot island breeze flew over the farm.\r\nNext thing you know, you are among friends.\r\n",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 159,
        "lesson_id": 24,
        "screen_title": "1",
        "screen_content": "a aq aqa qaq j ju juj uju just aqua\r\nquest cons toughs sequence thoughtless\r\nstaunch ghosts summer pounce afoul\r\ndifferentiated haircut",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 160,
        "lesson_id": 24,
        "screen_title": "2",
        "screen_content": "uncap runoff liquid sunned monitored\r\npopulous scudded unlearn fugitive\r\nfurnace fur level roguish illumined\r\nrectangular fortunate turbo mournful",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 161,
        "lesson_id": 24,
        "screen_title": "3",
        "screen_content": "acquisitiveness? economical?\r\npsychoanalytical \"cacophony\" ridiculous\r\ninsufficiencies: symphonic xylophonist\r\nfacetious face-saver perfectionism MacCracken Zygmont Corp.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 162,
        "lesson_id": 24,
        "screen_title": "4",
        "screen_content": "beechwood numeral universal hamstring\r\ncanon mockingbirds predation vote\r\nmaster nice aggregation sandpiper enter\r\nwide congregating weakened gravitation",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 163,
        "lesson_id": 24,
        "screen_title": "5",
        "screen_content": "explosive choir decrement witchcraft\r\nperception instruct consent evacuate\r\nefficient licked prancing stack\r\nexperiment teacup saccharides beseech acres counted backlash commence calling",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 164,
        "lesson_id": 24,
        "screen_title": "6",
        "screen_content": "She is testing the Xolophote Hypothesis\r\nby calibrating carboxypolypeptidase,\r\ndesoxycorticosterone and\r\nglucocorticoids for their effects on vasoconstriction and vasodilatation.",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 165,
        "lesson_id": 25,
        "screen_title": "1",
        "screen_content": "aaa 111 aaa 111 aaa 111 aaa 111 aa1 11a\r\nsss 222 ss2 22s\r\n1a a1 1a a1 1a a1 1a a1 1a aa1 11a\r\ns2 2s s2 2s s2 2s s2 2s s2 2s ss2 22s\r\n12 21 12 21 12 21 12 21 12 21 112 221",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 166,
        "lesson_id": 25,
        "screen_title": "2",
        "screen_content": "ddd 333 ddd 333 ddd 333 ddd 333 dd3 33d\r\nfff 444 fff 444 fff 444 fff 444 ff4 44f\r\nd3 3d d3 3d d3 3d d3 3d d3 3d dd3 33d\r\nf4 4f f4 4f f4 4f f4 4f f4 4f ff4 44f",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 167,
        "lesson_id": 25,
        "screen_title": "3",
        "screen_content": "fff 555 fff 555 fff 555 fff 555 ff5 55f\r\njjjj 665 jjjj 665 jjj 665 jjj 665 jj6\r\nf5 5f f5 5f f5 5f f5 5f f5 5f ff5 55f\r\nj6 6j j6 6j j6 6j j6 6j j6 6j jj6 66j",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 168,
        "lesson_id": 25,
        "screen_title": "4",
        "screen_content": "jjj 777 jjj 777 jjj 777 jjj 777 jj7 77j\r\nkkk 888 kkk 888 kkk 888 kkk 888 kk8 88k\r\nj7 7j j7 7j j7 7j j7 7j j7 7j jj7 77j\r\nk8 8k k8 8k k8 8k k8 8k k8 8k kk8 88k",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 169,
        "lesson_id": 25,
        "screen_title": "5",
        "screen_content": "111 999 111 999 111 999 111 999 119 991\r\n;;; 000 ;;; 000 ;;; 000 ;;; 000 ;; 0 00;\r\n19 91 19 91 19 91 19 91 19 91 119 991\r\n;0 0; ;0 0; ;0 0; ;0 0; ;0 0; ;; 0 00;",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 170,
        "lesson_id": 25,
        "screen_title": "6",
        "screen_content": "23424 03 4092 83 048203 09283 4082 2309\r\n2093 798167 9652345 1337 9877 243 68 4\r\n767 6747 685 4674 67464 2 2 2908 203 49\r\n02 3702 602 18 02 02",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 171,
        "lesson_id": 26,
        "screen_title": "1",
        "screen_content": "Dear Dan,\r\nYes, I came out of the corn back to the\r\ncity, both to draw and to do copy on\r\nthe new cars. To date, I am able to put\r\ncash in the bank and bear a bill or\r\ntwo. The new deed has done it.",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 172,
        "lesson_id": 26,
        "screen_title": "2",
        "screen_content": "Dear Sirs,\r\nI have just purchased an HP 2200x\r\ncomputer system and would like to order\r\ntwo boxes of diskettes for it. \r\nThis system uses 5 1/4 inch, hard-sectored,\r\nten-sector, single-sided,\r\nsingle-density diskettes. Enclosed is\r\nmy check for 45.00. Please rush this order as I\r\ncannot use my system before they arrive.",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 173,
        "lesson_id": 26,
        "screen_title": "3",
        "screen_content": "If you can do so,will you kindly let us know by return mail.\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 174,
        "lesson_id": 26,
        "screen_title": "4",
        "screen_content": "On each foot of my farm I felt free\r\nfrom fear. It gave me my fill of fun.\r\nfelt no fear of any fire in the fall.\r\nNow the fire is a fact and my farm is\r\ngone. Give me my full life, etc. The\r\ngame goes on.\r\nYours sincerely,\r\nTypist Pro",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 175,
        "lesson_id": 27,
        "screen_title": "1",
        "screen_content": "a !! ! a !!! a !!! a !!! a !!! a !!! a !!! a !!!\r\na!a a!a a!a a!a a!a a!a !a! !a! !a! !a!",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 176,
        "lesson_id": 27,
        "screen_title": "2",
        "screen_content": "s@@@ s@@@ sa@@ sa@@ s@@@ s@@@ @@@ @@@ s@s s@s s@s s@s s@s s@s @s@ @s@ @s@ @s@\r\nd### d### d### d### d### d### d### d### d#d d#d d#d d#d d#d d#d #d# #d# #d# #d#",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 177,
        "lesson_id": 27,
        "screen_title": "3",
        "screen_content": "f$$$ f$$$ f$$$ f$$$ f$$$ f$$$ f$$$ f$$$ f$f f$f f$f f$f f$f f$f $f$ $f$ $f$ $f$\r\nf % %% f %%% f%%% f%%% f%%% f%%%f%%% f%%% f%f f%f f%f f%f f%f f%f %f% %f% %f% %f%",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 178,
        "lesson_id": 27,
        "screen_title": "4",
        "screen_content": "j &&& j&&& j&&& j&&& j&&& j&&& j&&& j & & & j&j j&j j&j j&j j&j j&j &j& &j& & j& & \r\nk *** k *** k *** k *** k *** k *** k *** k *** k*k k*k k*k k*k k*k k*k *k* *k* *k* *k* j&",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 179,
        "lesson_id": 28,
        "screen_title": "1",
        "screen_content": "111111\r\n222222\r\n1212121\r\n2121212",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 180,
        "lesson_id": 28,
        "screen_title": "2",
        "screen_content": "3333333\r\n4444444\r\n34343434\r\n43434343\r\n23412431\r\n214324123",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 181,
        "lesson_id": 28,
        "screen_title": "3",
        "screen_content": "555555\r\n666666\r\n565656\r\n565656\r\n213456 526143",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 182,
        "lesson_id": 28,
        "screen_title": "4",
        "screen_content": "77777777\r\n88888888\r\n78787878\r\n87878787\r\n58425187423\r\n8854423672",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 183,
        "lesson_id": 28,
        "screen_title": "5",
        "screen_content": "999999999\r\n000000000\r\n990099009900\r\n90909090\r\n982546315\r\n7642831259",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 184,
        "lesson_id": 28,
        "screen_title": "6",
        "screen_content": "/////////\r\n*********\r\n---------\r\n+++++++++\r\n21-04-1999\r\n21/04/1999\r\n2022-02\r\n23*45\r\n58-56\r\n96+8\r\n254+658",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 185,
        "lesson_id": 4,
        "screen_title": "3",
        "screen_content": "\u0c85\u0c86\u0c87\r\n\u0c88\u0c89\u0c8a\r\n\u0c8b\u0c8e\u0c8f\r\n\u0c90\u0c92\u0c93\r\n\u0c94\u0c85\u0c82\u0c85\u0c83\r\n\u0c85\u0c86\u0c87\r\n\u0c88\u0c89\u0c8a\r\n\u0c8b\u0c8e\u0c8f\r\n\u0c90\u0c92\u0c93\r\n\u0c94\u0c85\u0c82\u0c85\u0c83\r\n",
        "screen_type": "jump",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 186,
        "lesson_id": 4,
        "screen_title": "4",
        "screen_content": "\u0c85\u0c87\u0c89\u0c8e\u0c92\r\n\u0c86\u0c88\u0c8a\u0c8f\u0c93\r\n\u0c8b\u0c90\u0c94\u0c85\u0c82\u0c85\u0c83\r\n\u0c85\u0c89\u0c8f\u0c93\u0c85\u0c82\r\n\u0c86\u0c87\u0c8e\u0c90\u0c85\u0c83\r\n\u0c88\u0c8a\u0c8b\u0c92\u0c94\r\n\u0c85\u0c86\u0c87\u0c88\u0c89\r\n\u0c8a\u0c8b\u0c8e\u0c8f\u0c90\r\n",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 187,
        "lesson_id": 4,
        "screen_title": "5",
        "screen_content": "\u0c85\u0c86\u0c87\u0c88\u0c89\u0c8a\u0c8b\u0c8e\u0c8f\u0c90\u0c92\u0c93\u0c94\u0c85\u0c82\u0c85\u0c83\r\n\u0c85\u0c82\u0c85\u0c83\u0c94\u0c93\u0c92\u0c90\u0c8f\u0c8e\u0c8b\u0c8a\u0c89\u0c88\u0c87\u0c86\u0c85\r\n\u0c85\u0c86\u0c87\u0c88\u0c89\u0c8a\u0c8b\u0c8e\u0c8f\u0c90\u0c92\u0c93\u0c94\u0c85\u0c82\u0c85\u0c83\r\n\u0c94\u0c93\u0c92\u0c90\u0c8f\u0c8e\u0c8b\u0c8a\u0c89\u0c88\u0c87\u0c86\u0c85\u0c85\u0c82\u0c85\u0c83\r\n\u0c85\u0c87\u0c89\u0c8e\u0c92\u0c86\u0c88\u0c8a\u0c8f\u0c93\u0c8b\u0c90\u0c94\u0c85\u0c82\u0c85\u0c83\r\n",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 188,
        "lesson_id": 29,
        "screen_title": "1",
        "screen_content": "\u0c95\u0c95\u0c95\u0c95\u0c95\u0c95\u0c95\u0c95\r\n\u0c96\u0c96\u0c96\u0c96\u0c96\u0c96\u0c96\u0c96\r\n\u0c97\u0c97\u0c97\u0c97\u0c97\u0c97\u0c97\u0c97\r\n\u0c98\u0c98\u0c98\u0c98\u0c98\u0c98\u0c98\u0c98\r\n\u0c99\u0c99\u0c99\u0c99\u0c99\u0c99\u0c99\u0c99",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 189,
        "lesson_id": 29,
        "screen_title": "2",
        "screen_content": "\u0c95\u0c96\u0c95\u0c96\u0c95\u0c96\r\n\u0c97\u0c98\u0c97\u0c98\u0c97\u0c98\r\n\u0c98\u0c99\u0c98\u0c99\u0c98\u0c99\r\n\u0c95\u0c97\u0c95\u0c97\u0c95\u0c97\r\n\u0c96\u0c98\u0c96\u0c98\u0c96\u0c98\r\n\u0c97\u0c99\u0c97\u0c99\u0c97\u0c99\r\n",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 190,
        "lesson_id": 29,
        "screen_title": "3",
        "screen_content": "\u0c95\u0c96\u0c97\u0c98\u0c99\r\n\u0c96\u0c97\u0c98\u0c99\u0c95\r\n\u0c97\u0c98\u0c99\u0c95\u0c96\r\n\u0c98\u0c99\u0c95\u0c96\u0c97\r\n\u0c99\u0c95\u0c96\u0c97\u0c98",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 191,
        "lesson_id": 29,
        "screen_title": "4",
        "screen_content": "\u0c99\u0c98\u0c97\u0c96\u0c95\r\n\u0c99\u0c98\u0c97\u0c96\u0c95\r\n\u0c99\u0c98\u0c97\u0c96\u0c95\r\n\u0c99\u0c98\u0c97\u0c96\u0c95\r\n\u0c99\u0c98\u0c97\u0c96\u0c95",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 192,
        "lesson_id": 29,
        "screen_title": "5",
        "screen_content": "\u0c97\u0c95\u0c98\u0c96\u0c99\r\n\u0c96\u0c99\u0c95\u0c97\u0c98\r\n\u0c98\u0c97\u0c96\u0c95\u0c99\r\n\u0c95\u0c98\u0c99\u0c96\u0c97\r\n\u0c99\u0c96\u0c97\u0c98\u0c95\r\n\u0c97\u0c99\u0c95\u0c98\u0c96\r\n",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 193,
        "lesson_id": 30,
        "screen_title": "1",
        "screen_content": "\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e\r\n\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e\r\n\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e\r\n\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e\r\n\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 194,
        "lesson_id": 30,
        "screen_title": "2",
        "screen_content": "\u0c9a\u0c9a\u0c9a\u0c9a\u0c9a\u0c9a\u0c9a\u0c9a\r\n\u0c9b\u0c9b\u0c9b\u0c9b\u0c9b\u0c9b\u0c9b\u0c9b\r\n\u0c9c\u0c9c\u0c9c\u0c9c\u0c9c\u0c9c\u0c9c\u0c9c\r\n\u0c9d\u0c9d\u0c9d\u0c9d\u0c9d\u0c9d\u0c9d\u0c9d\r\n\u0c9e\u0c9e\u0c9e\u0c9e\u0c9e\u0c9e\u0c9e\u0c9e",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 195,
        "lesson_id": 30,
        "screen_title": "3",
        "screen_content": "\u0c9a\u0c9b\u0c9a\u0c9b\u0c9a\u0c9b\r\n\u0c9c\u0c9d\u0c9c\u0c9d\u0c9c\u0c9d\r\n\u0c9d\u0c9e\u0c9d\u0c9e\u0c9d\u0c9e\r\n\u0c9a\u0c9c\u0c9a\u0c9c\u0c9a\u0c9c\r\n\u0c9b\u0c9d\u0c9b\u0c9d\u0c9b\u0c9d\r\n\u0c9c\u0c9e\u0c9c\u0c9e\u0c9c\u0c9e\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 196,
        "lesson_id": 30,
        "screen_title": "4",
        "screen_content": "\u0c9a\u0c9b\u0c9c\u0c9d\u0c9e\r\n\u0c9b\u0c9c\u0c9d\u0c9e\u0c9a\r\n\u0c9c\u0c9d\u0c9e\u0c9a\u0c9b\r\n\u0c9d\u0c9e\u0c9a\u0c9b\u0c9c\r\n\u0c9e\u0c9a\u0c9b\u0c9c\u0c9d",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 197,
        "lesson_id": 30,
        "screen_title": "5",
        "screen_content": "\u0c9e\u0c9d\u0c9c\u0c9b\u0c9a\r\n\u0c9e\u0c9d\u0c9c\u0c9b\u0c9a\r\n\u0c9e\u0c9d\u0c9c\u0c9b\u0c9a\r\n\u0c9e\u0c9d\u0c9c\u0c9b\u0c9a\r\n\u0c9e\u0c9d\u0c9c\u0c9b\u0c9a",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 198,
        "lesson_id": 31,
        "screen_title": "1",
        "screen_content": "\u0c9f\u0ca0\u0ca1\u0ca2\u0ca3\r\n\u0c9f\u0ca0\u0ca1\u0ca2\u0ca3\r\n\u0c9f\u0ca0\u0ca1\u0ca2\u0ca3\r\n\u0c9f\u0ca0\u0ca1\u0ca2\u0ca3\r\n\u0c9f\u0ca0\u0ca1\u0ca2\u0ca3",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 199,
        "lesson_id": 31,
        "screen_title": "2",
        "screen_content": "\u0c9f\u0c9f\u0c9f\u0c9f\u0c9f\u0c9f\u0c9f\u0c9f\r\n\u0ca0\u0ca0\u0ca0\u0ca0\u0ca0\u0ca0\u0ca0\u0ca0\r\n\u0ca1\u0ca1\u0ca1\u0ca1\u0ca1\u0ca1\u0ca1\u0ca1\r\n\u0ca2\u0ca2\u0ca2\u0ca2\u0ca2\u0ca2\u0ca2\u0ca2\r\n\u0ca3\u0ca3\u0ca3\u0ca3\u0ca3\u0ca3\u0ca3\u0ca3",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 200,
        "lesson_id": 31,
        "screen_title": "3",
        "screen_content": "\u0c9f \u0ca0 \u0c9f \u0ca0 \u0c9f \u0ca0\r\n\u0ca1 \u0ca2 \u0ca1 \u0ca2 \u0ca1 \u0ca2\r\n\u0ca2 \u0ca3 \u0ca2 \u0ca3 \u0ca2 \u0ca3\r\n\u0c9f \u0ca1 \u0c9f \u0ca1 \u0c9f \u0ca1\r\n\u0ca0 \u0ca2 \u0ca0 \u0ca2 \u0ca0 \u0ca2\r\n\r\n\u0ca1 \u0ca3 \u0ca1 \u0ca3 \u0ca1 \u0ca3",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 201,
        "lesson_id": 31,
        "screen_title": "4",
        "screen_content": "\u0c9f \u0ca0 \u0ca1 \u0ca2 \u0ca3\r\n\u0ca0 \u0ca1 \u0ca2 \u0ca3 \u0c9f\r\n\u0ca1 \u0ca2 \u0ca3 \u0c9f \u0ca0\r\n\u0ca2 \u0ca3 \u0c9f \u0ca0 \u0ca1\r\n\u0ca3 \u0c9f \u0ca0 \u0ca1 \u0ca2",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 202,
        "lesson_id": 31,
        "screen_title": "5",
        "screen_content": "\u0ca3 \u0ca2 \u0ca1 \u0ca0 \u0c9f\r\n\u0ca3 \u0ca2 \u0ca1 \u0ca0 \u0c9f\r\n\u0ca3 \u0ca2 \u0ca1 \u0ca0 \u0c9f\r\n\u0ca3 \u0ca2 \u0ca1 \u0ca0 \u0c9f\r\n\u0ca3 \u0ca2 \u0ca1 \u0ca0 \u0c9f",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 203,
        "lesson_id": 32,
        "screen_title": "1",
        "screen_content": "\u0ca4\u0ca5\u0ca6\u0ca7\u0ca8\r\n\u0ca4\u0ca5\u0ca6\u0ca7\u0ca8\r\n\u0ca4\u0ca5\u0ca6\u0ca7\u0ca8\r\n\u0ca4\u0ca5\u0ca6\u0ca7\u0ca8\r\n\u0ca4\u0ca5\u0ca6\u0ca7\u0ca8",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 204,
        "lesson_id": 32,
        "screen_title": "2",
        "screen_content": "\u0ca4\u0ca4\u0ca4\u0ca4\u0ca4\u0ca4\u0ca4\u0ca4\r\n\u0ca5\u0ca5\u0ca5\u0ca5\u0ca5\u0ca5\u0ca5\u0ca5\r\n\u0ca6\u0ca6\u0ca6\u0ca6\u0ca6\u0ca6\u0ca6\u0ca6\r\n\u0ca7\u0ca7\u0ca7\u0ca7\u0ca7\u0ca7\u0ca7\u0ca7\r\n\u0ca8\u0ca8\u0ca8\u0ca8\u0ca8\u0ca8\u0ca8\u0ca8",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 205,
        "lesson_id": 32,
        "screen_title": "3",
        "screen_content": "\u0ca4 \u0ca5 \u0ca4 \u0ca5 \u0ca4 \u0ca5\r\n\u0ca6 \u0ca7 \u0ca6 \u0ca7 \u0ca6 \u0ca7\r\n\u0ca7 \u0ca8 \u0ca7 \u0ca8 \u0ca7 \u0ca8\r\n\u0ca4 \u0ca6 \u0ca4 \u0ca6 \u0ca4 \u0ca6\r\n\u0ca5 \u0ca7 \u0ca5 \u0ca7 \u0ca5 \u0ca7\r\n\r\n\u0ca6 \u0ca8 \u0ca6 \u0ca8 \u0ca6 \u0ca8",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 206,
        "lesson_id": 32,
        "screen_title": "4",
        "screen_content": "\u0ca4 \u0ca5 \u0ca6 \u0ca7 \u0ca8\r\n\u0ca5 \u0ca6 \u0ca7 \u0ca8 \u0ca4\r\n\u0ca6 \u0ca7 \u0ca8 \u0ca4 \u0ca5\r\n\u0ca7 \u0ca8 \u0ca4 \u0ca5 \u0ca6\r\n\u0ca8 \u0ca4 \u0ca5 \u0ca6 \u0ca7",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 207,
        "lesson_id": 32,
        "screen_title": "5",
        "screen_content": "\u0ca8 \u0ca7 \u0ca6 \u0ca5 \u0ca4\r\n\u0ca8 \u0ca7 \u0ca6 \u0ca5 \u0ca4\r\n\u0ca8 \u0ca7 \u0ca6 \u0ca5 \u0ca4\r\n\u0ca8 \u0ca7 \u0ca6 \u0ca5 \u0ca4\r\n\u0ca8 \u0ca7 \u0ca6 \u0ca5 \u0ca4",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 208,
        "lesson_id": 33,
        "screen_title": "1",
        "screen_content": "\u0caa\u0cab\u0cac\u0cad\u0cae\r\n\u0caa\u0cab\u0cac\u0cad\u0cae\r\n\u0caa\u0cab\u0cac\u0cad\u0cae\r\n\u0caa\u0cab\u0cac\u0cad\u0cae\r\n\u0caa\u0cab\u0cac\u0cad\u0cae",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 209,
        "lesson_id": 33,
        "screen_title": "2",
        "screen_content": "\u0caa\u0caa\u0caa\u0caa\u0caa\u0caa\u0caa\u0caa\r\n\u0cab\u0cab\u0cab\u0cab\u0cab\u0cab\u0cab\u0cab\r\n\u0cac\u0cac\u0cac\u0cac\u0cac\u0cac\u0cac\u0cac\r\n\u0cad\u0cad\u0cad\u0cad\u0cad\u0cad\u0cad\u0cad\r\n\u0cae\u0cae\u0cae\u0cae\u0cae\u0cae\u0cae\u0cae\r\n",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 210,
        "lesson_id": 33,
        "screen_title": "3",
        "screen_content": "\u0caa \u0cab \u0caa \u0cab \u0caa \u0cab\r\n\u0cac \u0cad \u0cac \u0cad \u0cac \u0cad\r\n\u0cad \u0cae \u0cad \u0cae \u0cad \u0cae\r\n\u0caa \u0cac \u0caa \u0cac \u0caa \u0cac\r\n\u0cab \u0cad \u0cab \u0cad \u0cab \u0cad\r\n\r\n\u0cac \u0cae \u0cac \u0cae \u0cac \u0cae",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 211,
        "lesson_id": 33,
        "screen_title": "4",
        "screen_content": "\u0caa \u0cab \u0cac \u0cad \u0cae\r\n\u0cab \u0cac \u0cad \u0cae \u0caa\r\n\u0cac \u0cad \u0cae \u0caa \u0cab\r\n\u0cad \u0cae \u0caa \u0cab \u0cac\r\n\u0cae \u0caa \u0cab \u0cac \u0cad",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 212,
        "lesson_id": 33,
        "screen_title": "5",
        "screen_content": "\u0cae \u0cad \u0cac \u0cab \u0caa\r\n\u0cae \u0cad \u0cac \u0cab \u0caa\r\n\u0cae \u0cad \u0cac \u0cab \u0caa\r\n\u0cae \u0cad \u0cac \u0cab \u0caa\r\n\u0cae \u0cad \u0cac \u0cab \u0caa",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 213,
        "lesson_id": 34,
        "screen_title": "1",
        "screen_content": "\u0caf\u0cb0\u0cb2\u0cb5\u0cb6\u0cb7\u0cb8\u0cb9\u0cb3\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\r\n\u0caf\u0cb0\u0cb2\u0cb5\u0cb6\u0cb7\u0cb8\u0cb9\u0cb3\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\r\n\u0caf\u0cb0\u0cb2\u0cb5\u0cb6\u0cb7\u0cb8\u0cb9\u0cb3\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\r\n\u0caf\u0cb0\u0cb2\u0cb5\u0cb6\u0cb7\u0cb8\u0cb9\u0cb3\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 214,
        "lesson_id": 34,
        "screen_title": "2",
        "screen_content": "\u0caf\u0caf\u0caf\u0caf\u0caf\u0caf\r\n\u0cb0\u0cb0\u0cb0\u0cb0\u0cb0\u0cb0\r\n\u0cb2\u0cb2\u0cb2\u0cb2\u0cb2\u0cb2\r\n\u0cb5\u0cb5\u0cb5\u0cb5\u0cb5\u0cb5\r\n\u0cb6\u0cb6\u0cb6\u0cb6\u0cb6\u0cb6\r\n\u0cb7\u0cb7\u0cb7\u0cb7\u0cb7\u0cb7\r\n\u0cb8\u0cb8\u0cb8\u0cb8\u0cb8\u0cb8\r\n\u0cb9\u0cb9\u0cb9\u0cb9\u0cb9\u0cb9\r\n\u0cb3\u0cb3\u0cb3\u0cb3\u0cb3\u0cb3\r\n\u0c95\u0ccd\u0cb7\u0c95\u0ccd\u0cb7\u0c95\u0ccd\u0cb7\u0c95\u0ccd\u0cb7\u0c95\u0ccd\u0cb7\u0c95\u0ccd\u0cb7\r\n\u0c9c\u0ccd\u0c9e\u0c9c\u0ccd\u0c9e\u0c9c\u0ccd\u0c9e\u0c9c\u0ccd\u0c9e\u0c9c\u0ccd\u0c9e\u0c9c\u0ccd\u0c9e\r\n",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 215,
        "lesson_id": 34,
        "screen_title": "3",
        "screen_content": "\u0caf\u0cb0\u0caf\u0cb0\u0caf\u0cb0\r\n\u0cb2\u0cb5\u0cb2\u0cb5\u0cb2\u0cb5\r\n\u0cb6\u0cb7\u0cb6\u0cb7\u0cb6\u0cb7\r\n\u0cb8\u0cb9\u0cb8\u0cb9\u0cb8\u0cb9\r\n\u0cb3\u0c95\u0ccd\u0cb7\u0cb3\u0c95\u0ccd\u0cb7\u0cb3\u0c95\u0ccd\u0cb7\r\n\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\u0c95\u0ccd\u0cb7\u0c9c\u0ccd\u0c9e\r\n\u0caf\u0cb2\u0caf\u0cb2\r\n\u0cb0\u0cb5\u0cb0\u0cb5\r\n\u0cb6\u0cb8\u0cb6\u0cb8\r\n\u0cb9\u0c9c\u0ccd\u0c9e\u0cb9\u0c9c\u0ccd\u0c9e\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 216,
        "lesson_id": 35,
        "screen_title": "1",
        "screen_content": "\u0c95\u0c95\u0cbe\u0c95\u0cbf\u0c95\u0cc0\u0c95\u0cc1\u0c95\u0cc2\u0c95\u0cc3\u0c95\u0cc6\u0c95\u0cc7\u0c95\u0cc8\u0c95\u0cca\u0c95\u0ccb\u0c95\u0ccc\u0c95\u0c82\u0c95\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 217,
        "lesson_id": 35,
        "screen_title": "2",
        "screen_content": "\u0c95\u0c95\u0cbe\u0c95\u0cbf\u0c95\u0cc0\u0c95\u0cc1\u0c95\u0cc2\u0c95\u0cc3\u0c95\u0cc6\u0c95\u0cc7\u0c95\u0cc8\u0c95\u0cca\u0c95\u0ccb\u0c95\u0ccc\u0c95\u0c82\u0c95\u0c83\r\n\u0c95\u0c95\u0cbe\u0c95\u0cbf\u0c95\u0cc0\u0c95\u0cc1\u0c95\u0cc2\u0c95\u0cc3\u0c95\u0cc6\u0c95\u0cc7\u0c95\u0cc8\u0c95\u0cca\u0c95\u0ccb\u0c95\u0ccc\u0c95\u0c82\u0c95\u0c83",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 218,
        "lesson_id": 35,
        "screen_title": "3",
        "screen_content": "\u0c96\u0c96\u0cbe\u0c96\u0cbf\u0c96\u0cc0\u0c96\u0cc1\u0c96\u0cc2\u0c96\u0cc3\u0c96\u0cc6\u0c96\u0cc7\u0c96\u0cc8\u0c96\u0cca\u0c96\u0ccb\u0c96\u0ccc\u0c96\u0c82\u0c96\u0c83",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 219,
        "lesson_id": 35,
        "screen_title": "4",
        "screen_content": "\u0c96\u0c96\u0cbe\u0c96\u0cbf\u0c96\u0cc0\u0c96\u0cc1\u0c96\u0cc2\u0c96\u0cc3\u0c96\u0cc6\u0c96\u0cc7\u0c96\u0cc8\u0c96\u0cca\u0c96\u0ccb\u0c96\u0ccc\u0c96\u0c82\u0c96\u0c83\r\n\u0c96\u0c96\u0cbe\u0c96\u0cbf\u0c96\u0cc0\u0c96\u0cc1\u0c96\u0cc2\u0c96\u0cc3\u0c96\u0cc6\u0c96\u0cc7\u0c96\u0cc8\u0c96\u0cca\u0c96\u0ccb\u0c96\u0ccc\u0c96\u0c82\u0c96\u0c83\r\n\u0c96\u0c96\u0cbe\u0c96\u0cbf\u0c96\u0cc0\u0c96\u0cc1\u0c96\u0cc2\u0c96\u0cc3\u0c96\u0cc6\u0c96\u0cc7\u0c96\u0cc8\u0c96\u0cca\u0c96\u0ccb\u0c96\u0ccc\u0c96\u0c82\u0c96\u0c83",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 220,
        "lesson_id": 35,
        "screen_title": "5",
        "screen_content": "\u0c97\u0c97\u0cbe\u0c97\u0cbf\u0c97\u0cc0\u0c97\u0cc1\u0c97\u0cc2\u0c97\u0cc3\u0c97\u0cc6\u0c97\u0cc7\u0c97\u0cc8\u0c97\u0cca\u0c97\u0ccb\u0c97\u0ccc\u0c97\u0c82\u0c97\u0c83",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 221,
        "lesson_id": 35,
        "screen_title": "6",
        "screen_content": "\u0c97\u0c97\u0cbe\u0c97\u0cbf\u0c97\u0cc0\u0c97\u0cc1\u0c97\u0cc2\u0c97\u0cc3\u0c97\u0cc6\u0c97\u0cc7\u0c97\u0cc8\u0c97\u0cca\u0c97\u0ccb\u0c97\u0ccc\u0c97\u0c82\u0c97\u0c83\r\n\u0c97\u0c97\u0cbe\u0c97\u0cbf\u0c97\u0cc0\u0c97\u0cc1\u0c97\u0cc2\u0c97\u0cc3\u0c97\u0cc6\u0c97\u0cc7\u0c97\u0cc8\u0c97\u0cca\u0c97\u0ccb\u0c97\u0ccc\u0c97\u0c82\u0c97\u0c83\r\n\u0c97\u0c97\u0cbe\u0c97\u0cbf\u0c97\u0cc0\u0c97\u0cc1\u0c97\u0cc2\u0c97\u0cc3\u0c97\u0cc6\u0c97\u0cc7\u0c97\u0cc8\u0c97\u0cca\u0c97\u0ccb\u0c97\u0ccc\u0c97\u0c82\u0c97\u0c83",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 222,
        "lesson_id": 35,
        "screen_title": "7",
        "screen_content": "\u0c98\u0c98\u0cbe\u0c98\u0cbf\u0c98\u0cc0\u0c98\u0cc1\u0c98\u0cc2\u0c98\u0cc3\u0c98\u0cc6\u0c98\u0cc7\u0c98\u0cc8\u0c98\u0cca\u0c98\u0ccb\u0c98\u0ccc\u0c98\u0c82\u0c98\u0c83",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 223,
        "lesson_id": 35,
        "screen_title": "8",
        "screen_content": "\u0c98\u0c98\u0cbe\u0c98\u0cbf\u0c98\u0cc0\u0c98\u0cc1\u0c98\u0cc2\u0c98\u0cc3\u0c98\u0cc6\u0c98\u0cc7\u0c98\u0cc8\u0c98\u0cca\u0c98\u0ccb\u0c98\u0ccc\u0c98\u0c82\u0c98\u0c83\r\n\u0c98\u0c98\u0cbe\u0c98\u0cbf\u0c98\u0cc0\u0c98\u0cc1\u0c98\u0cc2\u0c98\u0cc3\u0c98\u0cc6\u0c98\u0cc7\u0c98\u0cc8\u0c98\u0cca\u0c98\u0ccb\u0c98\u0ccc\u0c98\u0c82\u0c98\u0c83\r\n\u0c98\u0c98\u0cbe\u0c98\u0cbf\u0c98\u0cc0\u0c98\u0cc1\u0c98\u0cc2\u0c98\u0cc3\u0c98\u0cc6\u0c98\u0cc7\u0c98\u0cc8\u0c98\u0cca\u0c98\u0ccb\u0c98\u0ccc\u0c98\u0c82\u0c98\u0c83\r\n",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 224,
        "lesson_id": 36,
        "screen_title": "1",
        "screen_content": "\u0c9a\u0c9a\u0cbe\u0c9a\u0cbf\u0c9a\u0cc0\u0c9a\u0cc1\u0c9a\u0cc2\u0c9a\u0cc3\u0c9a\u0cc6\u0c9a\u0cc7\u0c9a\u0cc8\u0c9a\u0cca\u0c9a\u0ccb\u0c9a\u0ccc\u0c9a\u0c82\u0c9a\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 225,
        "lesson_id": 36,
        "screen_title": "2",
        "screen_content": "\u0c9a\u0c9a\u0cbe\u0c9a\u0cbf\u0c9a\u0cc0\u0c9a\u0cc1\u0c9a\u0cc2\u0c9a\u0cc3\u0c9a\u0cc6\u0c9a\u0cc7\u0c9a\u0cc8\u0c9a\u0cca\u0c9a\u0ccb\u0c9a\u0ccc\u0c9a\u0c82\u0c9a\u0c83\r\n\u0c9a\u0c9a\u0cbe\u0c9a\u0cbf\u0c9a\u0cc0\u0c9a\u0cc1\u0c9a\u0cc2\u0c9a\u0cc3\u0c9a\u0cc6\u0c9a\u0cc7\u0c9a\u0cc8\u0c9a\u0cca\u0c9a\u0ccb\u0c9a\u0ccc\u0c9a\u0c82\u0c9a\u0c83",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 226,
        "lesson_id": 36,
        "screen_title": "3",
        "screen_content": "\u0c9b\u0c9b\u0cbe\u0c9b\u0cbf\u0c9b\u0cc0\u0c9b\u0cc1\u0c9b\u0cc2\u0c9b\u0cc3\u0c9b\u0cc6\u0c9b\u0cc7\u0c9b\u0cc8\u0c9b\u0cca\u0c9b\u0ccb\u0c9b\u0ccc\u0c9b\u0c82\u0c9b\u0c83",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 227,
        "lesson_id": 36,
        "screen_title": "4",
        "screen_content": "\u0c9b\u0c9b\u0cbe\u0c9b\u0cbf\u0c9b\u0cc0\u0c9b\u0cc1\u0c9b\u0cc2\u0c9b\u0cc3\u0c9b\u0cc6\u0c9b\u0cc7\u0c9b\u0cc8\u0c9b\u0cca\u0c9b\u0ccb\u0c9b\u0ccc\u0c9b\u0c82\u0c9b\u0c83\r\n\u0c9b\u0c9b\u0cbe\u0c9b\u0cbf\u0c9b\u0cc0\u0c9b\u0cc1\u0c9b\u0cc2\u0c9b\u0cc3\u0c9b\u0cc6\u0c9b\u0cc7\u0c9b\u0cc8\u0c9b\u0cca\u0c9b\u0ccb\u0c9b\u0ccc\u0c9b\u0c82\u0c9b\u0c83",
        "screen_type": "block",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 228,
        "lesson_id": 36,
        "screen_title": "5",
        "screen_content": "\u0c9c\u0c9c\u0cbe\u0c9c\u0cbf\u0c9c\u0cc0\u0c9c\u0cc1\u0c9c\u0cc2\u0c9c\u0cc3\u0c9c\u0cc6\u0c9c\u0cc7\u0c9c\u0cc8\u0c9c\u0cca\u0c9c\u0ccb\u0c9c\u0ccc\u0c9c\u0c82\u0c9c\u0c83",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 229,
        "lesson_id": 36,
        "screen_title": "6",
        "screen_content": "\u0c9c\u0c9c\u0cbe\u0c9c\u0cbf\u0c9c\u0cc0\u0c9c\u0cc1\u0c9c\u0cc2\u0c9c\u0cc3\u0c9c\u0cc6\u0c9c\u0cc7\u0c9c\u0cc8\u0c9c\u0cca\u0c9c\u0ccb\u0c9c\u0ccc\u0c9c\u0c82\u0c9c\u0c83\r\n\u0c9c\u0c9c\u0cbe\u0c9c\u0cbf\u0c9c\u0cc0\u0c9c\u0cc1\u0c9c\u0cc2\u0c9c\u0cc3\u0c9c\u0cc6\u0c9c\u0cc7\u0c9c\u0cc8\u0c9c\u0cca\u0c9c\u0ccb\u0c9c\u0ccc\u0c9c\u0c82\u0c9c\u0c83",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 230,
        "lesson_id": 36,
        "screen_title": "7",
        "screen_content": "\u0c9d\u0c9d\u0cbe\u0c9d\u0cbf\u0c9d\u0cc0\u0c9d\u0cc1\u0c9d\u0cc2\u0c9d\u0cc3\u0c9d\u0cc6\u0c9d\u0cc7\u0c9d\u0cc8\u0c9d\u0cca\u0c9d\u0ccb\u0c9d\u0ccc\u0c9d\u0c82\u0c9d\u0c83",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 231,
        "lesson_id": 36,
        "screen_title": "8",
        "screen_content": "\u0c9d\u0c9d\u0cbe\u0c9d\u0cbf\u0c9d\u0cc0\u0c9d\u0cc1\u0c9d\u0cc2\u0c9d\u0cc3\u0c9d\u0cc6\u0c9d\u0cc7\u0c9d\u0cc8\u0c9d\u0cca\u0c9d\u0ccb\u0c9d\u0ccc\u0c9d\u0c82\u0c9d\u0c83\r\n\u0c9d\u0c9d\u0cbe\u0c9d\u0cbf\u0c9d\u0cc0\u0c9d\u0cc1\u0c9d\u0cc2\u0c9d\u0cc3\u0c9d\u0cc6\u0c9d\u0cc7\u0c9d\u0cc8\u0c9d\u0cca\u0c9d\u0ccb\u0c9d\u0ccc\u0c9d\u0c82\u0c9d\u0c83",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 232,
        "lesson_id": 37,
        "screen_title": "1",
        "screen_content": "\u0c9f\u0c9f\u0cbe\u0c9f\u0cbf\u0c9f\u0cc0\u0c9f\u0cc1\u0c9f\u0cc2\u0c9f\u0cc3\u0c9f\u0cc6\u0c9f\u0cc7\u0c9f\u0cc8\u0c9f\u0cca\u0c9f\u0ccb\u0c9f\u0ccc\u0c9f\u0c82\u0c9f\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 233,
        "lesson_id": 37,
        "screen_title": "2",
        "screen_content": "\u0c9f\u0c9f\u0cbe\u0c9f\u0cbf\u0c9f\u0cc0\u0c9f\u0cc1\u0c9f\u0cc2\u0c9f\u0cc3\u0c9f\u0cc6\u0c9f\u0cc7\u0c9f\u0cc8\u0c9f\u0cca\u0c9f\u0ccb\u0c9f\u0ccc\u0c9f\u0c82\u0c9f\u0c83\r\n\u0c9f\u0c9f\u0cbe\u0c9f\u0cbf\u0c9f\u0cc0\u0c9f\u0cc1\u0c9f\u0cc2\u0c9f\u0cc3\u0c9f\u0cc6\u0c9f\u0cc7\u0c9f\u0cc8\u0c9f\u0cca\u0c9f\u0ccb\u0c9f\u0ccc\u0c9f\u0c82\u0c9f\u0c83",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 234,
        "lesson_id": 37,
        "screen_title": "3",
        "screen_content": "\u0ca0\u0ca0\u0cbe\u0ca0\u0cbf\u0ca0\u0cc0\u0ca0\u0cc1\u0ca0\u0cc2\u0ca0\u0cc3\u0ca0\u0cc6\u0ca0\u0cc7\u0ca0\u0cc8\u0ca0\u0cca\u0ca0\u0ccb\u0ca0\u0ccc\u0ca0\u0c82\u0ca0\u0c83",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 235,
        "lesson_id": 37,
        "screen_title": "4",
        "screen_content": "\u0ca0\u0ca0\u0cbe\u0ca0\u0cbf\u0ca0\u0cc0\u0ca0\u0cc1\u0ca0\u0cc2\u0ca0\u0cc3\u0ca0\u0cc6\u0ca0\u0cc7\u0ca0\u0cc8\u0ca0\u0cca\u0ca0\u0ccb\u0ca0\u0ccc\u0ca0\u0c82\u0ca0\u0c83\r\n\u0ca0\u0ca0\u0cbe\u0ca0\u0cbf\u0ca0\u0cc0\u0ca0\u0cc1\u0ca0\u0cc2\u0ca0\u0cc3\u0ca0\u0cc6\u0ca0\u0cc7\u0ca0\u0cc8\u0ca0\u0cca\u0ca0\u0ccb\u0ca0\u0ccc\u0ca0\u0c82\u0ca0\u0c83",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 236,
        "lesson_id": 37,
        "screen_title": "5",
        "screen_content": "\u0ca1\u0ca1\u0cbe\u0ca1\u0cbf\u0ca1\u0cc0\u0ca1\u0cc1\u0ca1\u0cc2\u0ca1\u0cc3\u0ca1\u0cc6\u0ca1\u0cc7\u0ca1\u0cc8\u0ca1\u0cca\u0ca1\u0ccb\u0ca1\u0ccc\u0ca1\u0c82\u0ca1\u0c83",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 237,
        "lesson_id": 37,
        "screen_title": "6",
        "screen_content": "\u0ca1\u0ca1\u0cbe\u0ca1\u0cbf\u0ca1\u0cc0\u0ca1\u0cc1\u0ca1\u0cc2\u0ca1\u0cc3\u0ca1\u0cc6\u0ca1\u0cc7\u0ca1\u0cc8\u0ca1\u0cca\u0ca1\u0ccb\u0ca1\u0ccc\u0ca1\u0c82\u0ca1\u0c83\r\n\u0ca1\u0ca1\u0cbe\u0ca1\u0cbf\u0ca1\u0cc0\u0ca1\u0cc1\u0ca1\u0cc2\u0ca1\u0cc3\u0ca1\u0cc6\u0ca1\u0cc7\u0ca1\u0cc8\u0ca1\u0cca\u0ca1\u0ccb\u0ca1\u0ccc\u0ca1\u0c82\u0ca1\u0c83",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 238,
        "lesson_id": 37,
        "screen_title": "7",
        "screen_content": "\u0ca2\u0ca2\u0cbe\u0ca2\u0cbf\u0ca2\u0cc0\u0ca2\u0cc1\u0ca2\u0cc2\u0ca2\u0cc3\u0ca2\u0cc6\u0ca2\u0cc7\u0ca2\u0cc8\u0ca2\u0cca\u0ca2\u0ccb\u0ca2\u0ccc\u0ca2\u0c82\u0ca2\u0c83",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 239,
        "lesson_id": 37,
        "screen_title": "8",
        "screen_content": "\u0ca2\u0ca2\u0cbe\u0ca2\u0cbf\u0ca2\u0cc0\u0ca2\u0cc1\u0ca2\u0cc2\u0ca2\u0cc3\u0ca2\u0cc6\u0ca2\u0cc7\u0ca2\u0cc8\u0ca2\u0cca\u0ca2\u0ccb\u0ca2\u0ccc\u0ca2\u0c82\u0ca2\u0c83\r\n\u0ca2\u0ca2\u0cbe\u0ca2\u0cbf\u0ca2\u0cc0\u0ca2\u0cc1\u0ca2\u0cc2\u0ca2\u0cc3\u0ca2\u0cc6\u0ca2\u0cc7\u0ca2\u0cc8\u0ca2\u0cca\u0ca2\u0ccb\u0ca2\u0ccc\u0ca2\u0c82\u0ca2\u0c83",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 240,
        "lesson_id": 37,
        "screen_title": "9",
        "screen_content": "\u0ca3\u0ca3\u0cbe\u0ca3\u0cbf\u0ca3\u0cc0\u0ca3\u0cc1\u0ca3\u0cc2\u0ca3\u0cc3\u0ca3\u0cc6\u0ca3\u0cc7\u0ca3\u0cc8\u0ca3\u0cca\u0ca3\u0ccb\u0ca3\u0ccc\u0ca3\u0c82\u0ca3\u0c83",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 241,
        "lesson_id": 37,
        "screen_title": "10",
        "screen_content": "\u0ca3\u0ca3\u0cbe\u0ca3\u0cbf\u0ca3\u0cc0\u0ca3\u0cc1\u0ca3\u0cc2\u0ca3\u0cc3\u0ca3\u0cc6\u0ca3\u0cc7\u0ca3\u0cc8\u0ca3\u0cca\u0ca3\u0ccb\u0ca3\u0ccc\u0ca3\u0c82\u0ca3\u0c83\r\n\u0ca3\u0ca3\u0cbe\u0ca3\u0cbf\u0ca3\u0cc0\u0ca3\u0cc1\u0ca3\u0cc2\u0ca3\u0cc3\u0ca3\u0cc6\u0ca3\u0cc7\u0ca3\u0cc8\u0ca3\u0cca\u0ca3\u0ccb\u0ca3\u0ccc\u0ca3\u0c82\u0ca3\u0c83",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 242,
        "lesson_id": 38,
        "screen_title": "1",
        "screen_content": "\u0ca4\u0ca4\u0cbe\u0ca4\u0cbf\u0ca4\u0cc0\u0ca4\u0cc1\u0ca4\u0cc2\u0ca4\u0cc3\u0ca4\u0cc6\u0ca4\u0cc7\u0ca4\u0cc8\u0ca4\u0cca\u0ca4\u0ccb\u0ca4\u0ccc\u0ca4\u0c82\u0ca4\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 243,
        "lesson_id": 38,
        "screen_title": "2",
        "screen_content": "\u0ca4\u0ca4\u0cbe\u0ca4\u0cbf\u0ca4\u0cc0\u0ca4\u0cc1\u0ca4\u0cc2\u0ca4\u0cc3\u0ca4\u0cc6\u0ca4\u0cc7\u0ca4\u0cc8\u0ca4\u0cca\u0ca4\u0ccb\u0ca4\u0ccc\u0ca4\u0c82\u0ca4\u0c83\r\n\u0ca4\u0ca4\u0cbe\u0ca4\u0cbf\u0ca4\u0cc0\u0ca4\u0cc1\u0ca4\u0cc2\u0ca4\u0cc3\u0ca4\u0cc6\u0ca4\u0cc7\u0ca4\u0cc8\u0ca4\u0cca\u0ca4\u0ccb\u0ca4\u0ccc\u0ca4\u0c82\u0ca4\u0c83",
        "screen_type": "block",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 244,
        "lesson_id": 38,
        "screen_title": "3",
        "screen_content": "\u0ca5\u0ca5\u0cbe\u0ca5\u0cbf\u0ca5\u0cc0\u0ca5\u0cc1\u0ca5\u0cc2\u0ca5\u0cc3\u0ca5\u0cc6\u0ca5\u0cc7\u0ca5\u0cc8\u0ca5\u0cca\u0ca5\u0ccb\u0ca5\u0ccc\u0ca5\u0c82\u0ca5\u0c83",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 245,
        "lesson_id": 38,
        "screen_title": "4",
        "screen_content": "\u0ca5\u0ca5\u0cbe\u0ca5\u0cbf\u0ca5\u0cc0\u0ca5\u0cc1\u0ca5\u0cc2\u0ca5\u0cc3\u0ca5\u0cc6\u0ca5\u0cc7\u0ca5\u0cc8\u0ca5\u0cca\u0ca5\u0ccb\u0ca5\u0ccc\u0ca5\u0c82\u0ca5\u0c83\r\n\u0ca5\u0ca5\u0cbe\u0ca5\u0cbf\u0ca5\u0cc0\u0ca5\u0cc1\u0ca5\u0cc2\u0ca5\u0cc3\u0ca5\u0cc6\u0ca5\u0cc7\u0ca5\u0cc8\u0ca5\u0cca\u0ca5\u0ccb\u0ca5\u0ccc\u0ca5\u0c82\u0ca5\u0c83",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 246,
        "lesson_id": 38,
        "screen_title": "5",
        "screen_content": "\u0ca6\u0ca6\u0cbe\u0ca6\u0cbf\u0ca6\u0cc0\u0ca6\u0cc1\u0ca6\u0cc2\u0ca6\u0cc3\u0ca6\u0cc6\u0ca6\u0cc7\u0ca6\u0cc8\u0ca6\u0cca\u0ca6\u0ccb\u0ca6\u0ccc\u0ca6\u0c82\u0ca6\u0c83",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 247,
        "lesson_id": 38,
        "screen_title": "6",
        "screen_content": "\u0ca6\u0ca6\u0cbe\u0ca6\u0cbf\u0ca6\u0cc0\u0ca6\u0cc1\u0ca6\u0cc2\u0ca6\u0cc3\u0ca6\u0cc6\u0ca6\u0cc7\u0ca6\u0cc8\u0ca6\u0cca\u0ca6\u0ccb\u0ca6\u0ccc\u0ca6\u0c82\u0ca6\u0c83\r\n\u0ca6\u0ca6\u0cbe\u0ca6\u0cbf\u0ca6\u0cc0\u0ca6\u0cc1\u0ca6\u0cc2\u0ca6\u0cc3\u0ca6\u0cc6\u0ca6\u0cc7\u0ca6\u0cc8\u0ca6\u0cca\u0ca6\u0ccb\u0ca6\u0ccc\u0ca6\u0c82\u0ca6\u0c83",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 248,
        "lesson_id": 38,
        "screen_title": "7",
        "screen_content": "\u0ca7\u0ca7\u0cbe\u0ca7\u0cbf\u0ca7\u0cc0\u0ca7\u0cc1\u0ca7\u0cc2\u0ca7\u0cc3\u0ca7\u0cc6\u0ca7\u0cc7\u0ca7\u0cc8\u0ca7\u0cca\u0ca7\u0ccb\u0ca7\u0ccc\u0ca7\u0c82\u0ca7\u0c83",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 249,
        "lesson_id": 38,
        "screen_title": "8",
        "screen_content": "\u0ca7\u0ca7\u0cbe\u0ca7\u0cbf\u0ca7\u0cc0\u0ca7\u0cc1\u0ca7\u0cc2\u0ca7\u0cc3\u0ca7\u0cc6\u0ca7\u0cc7\u0ca7\u0cc8\u0ca7\u0cca\u0ca7\u0ccb\u0ca7\u0ccc\u0ca7\u0c82\u0ca7\u0c83\r\n\u0ca7\u0ca7\u0cbe\u0ca7\u0cbf\u0ca7\u0cc0\u0ca7\u0cc1\u0ca7\u0cc2\u0ca7\u0cc3\u0ca7\u0cc6\u0ca7\u0cc7\u0ca7\u0cc8\u0ca7\u0cca\u0ca7\u0ccb\u0ca7\u0ccc\u0ca7\u0c82\u0ca7\u0c83",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 250,
        "lesson_id": 38,
        "screen_title": "9",
        "screen_content": "\u0ca8\u0ca8\u0cbe\u0ca8\u0cbf\u0ca8\u0cc0\u0ca8\u0cc1\u0ca8\u0cc2\u0ca8\u0cc3\u0ca8\u0cc6\u0ca8\u0cc7\u0ca8\u0cc8\u0ca8\u0cca\u0ca8\u0ccb\u0ca8\u0ccc\u0ca8\u0c82\u0ca8\u0c83",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 251,
        "lesson_id": 38,
        "screen_title": "10",
        "screen_content": "\u0ca8\u0ca8\u0cbe\u0ca8\u0cbf\u0ca8\u0cc0\u0ca8\u0cc1\u0ca8\u0cc2\u0ca8\u0cc3\u0ca8\u0cc6\u0ca8\u0cc7\u0ca8\u0cc8\u0ca8\u0cca\u0ca8\u0ccb\u0ca8\u0ccc\u0ca8\u0c82\u0ca8\u0c83\r\n\u0ca8\u0ca8\u0cbe\u0ca8\u0cbf\u0ca8\u0cc0\u0ca8\u0cc1\u0ca8\u0cc2\u0ca8\u0cc3\u0ca8\u0cc6\u0ca8\u0cc7\u0ca8\u0cc8\u0ca8\u0cca\u0ca8\u0ccb\u0ca8\u0ccc\u0ca8\u0c82\u0ca8\u0c83",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 252,
        "lesson_id": 39,
        "screen_title": "1",
        "screen_content": "\u0caa\u0caa\u0cbe\u0caa\u0cbf\u0caa\u0cc0\u0caa\u0cc1\u0caa\u0cc2\u0caa\u0cc3\u0caa\u0cc6\u0caa\u0cc7\u0caa\u0cc8\u0caa\u0cca\u0caa\u0ccb\u0caa\u0ccc\u0caa\u0c82\u0caa\u0c83",
        "screen_type": "block",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 253,
        "lesson_id": 39,
        "screen_title": "2",
        "screen_content": "\u0caa\u0caa\u0cbe\u0caa\u0cbf\u0caa\u0cc0\u0caa\u0cc1\u0caa\u0cc2\u0caa\u0cc3\u0caa\u0cc6\u0caa\u0cc7\u0caa\u0cc8\u0caa\u0cca\u0caa\u0ccb\u0caa\u0ccc\u0caa\u0c82\u0caa\u0c83\r\n\u0caa\u0caa\u0cbe\u0caa\u0cbf\u0caa\u0cc0\u0caa\u0cc1\u0caa\u0cc2\u0caa\u0cc3\u0caa\u0cc6\u0caa\u0cc7\u0caa\u0cc8\u0caa\u0cca\u0caa\u0ccb\u0caa\u0ccc\u0caa\u0c82\u0caa\u0c83",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 254,
        "lesson_id": 39,
        "screen_title": "3",
        "screen_content": "\u0cab\u0cab\u0cbe\u0cab\u0cbf\u0cab\u0cc0\u0cab\u0cc1\u0cab\u0cc2\u0cab\u0cc3\u0cab\u0cc6\u0cab\u0cc7\u0cab\u0cc8\u0cab\u0cca\u0cab\u0ccb\u0cab\u0ccc\u0cab\u0c82\u0cab\u0c83",
        "screen_type": "block",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 255,
        "lesson_id": 39,
        "screen_title": "4",
        "screen_content": "\u0cab\u0cab\u0cbe\u0cab\u0cbf\u0cab\u0cc0\u0cab\u0cc1\u0cab\u0cc2\u0cab\u0cc3\u0cab\u0cc6\u0cab\u0cc7\u0cab\u0cc8\u0cab\u0cca\u0cab\u0ccb\u0cab\u0ccc\u0cab\u0c82\u0cab\u0c83\r\n\u0cab\u0cab\u0cbe\u0cab\u0cbf\u0cab\u0cc0\u0cab\u0cc1\u0cab\u0cc2\u0cab\u0cc3\u0cab\u0cc6\u0cab\u0cc7\u0cab\u0cc8\u0cab\u0cca\u0cab\u0ccb\u0cab\u0ccc\u0cab\u0c82\u0cab\u0c83",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 256,
        "lesson_id": 39,
        "screen_title": "5",
        "screen_content": "\u0cac\u0cac\u0cbe\u0cac\u0cbf\u0cac\u0cc0\u0cac\u0cc1\u0cac\u0cc2\u0cac\u0cc3\u0cac\u0cc6\u0cac\u0cc7\u0cac\u0cc8\u0cac\u0cca\u0cac\u0ccb\u0cac\u0ccc\u0cac\u0c82\u0cac\u0c83",
        "screen_type": "block",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 257,
        "lesson_id": 39,
        "screen_title": "6",
        "screen_content": "\u0cac\u0cac\u0cbe\u0cac\u0cbf\u0cac\u0cc0\u0cac\u0cc1\u0cac\u0cc2\u0cac\u0cc3\u0cac\u0cc6\u0cac\u0cc7\u0cac\u0cc8\u0cac\u0cca\u0cac\u0ccb\u0cac\u0ccc\u0cac\u0c82\u0cac\u0c83\r\n\u0cac\u0cac\u0cbe\u0cac\u0cbf\u0cac\u0cc0\u0cac\u0cc1\u0cac\u0cc2\u0cac\u0cc3\u0cac\u0cc6\u0cac\u0cc7\u0cac\u0cc8\u0cac\u0cca\u0cac\u0ccb\u0cac\u0ccc\u0cac\u0c82\u0cac\u0c83",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 258,
        "lesson_id": 39,
        "screen_title": "7",
        "screen_content": "\u0cad\u0cad\u0cbe\u0cad\u0cbf\u0cad\u0cc0\u0cad\u0cc1\u0cad\u0cc2\u0cad\u0cc3\u0cad\u0cc6\u0cad\u0cc7\u0cad\u0cc8\u0cad\u0cca\u0cad\u0ccb\u0cad\u0ccc\u0cad\u0c82\u0cad\u0c83",
        "screen_type": "block",
        "display_order": 7,
        "status": "Active"
    },
    {
        "screen_id": 259,
        "lesson_id": 39,
        "screen_title": "8",
        "screen_content": "\u0cad\u0cad\u0cbe\u0cad\u0cbf\u0cad\u0cc0\u0cad\u0cc1\u0cad\u0cc2\u0cad\u0cc3\u0cad\u0cc6\u0cad\u0cc7\u0cad\u0cc8\u0cad\u0cca\u0cad\u0ccb\u0cad\u0ccc\u0cad\u0c82\u0cad\u0c83\r\n\u0cad\u0cad\u0cbe\u0cad\u0cbf\u0cad\u0cc0\u0cad\u0cc1\u0cad\u0cc2\u0cad\u0cc3\u0cad\u0cc6\u0cad\u0cc7\u0cad\u0cc8\u0cad\u0cca\u0cad\u0ccb\u0cad\u0ccc\u0cad\u0c82\u0cad\u0c83",
        "screen_type": "paragraph",
        "display_order": 8,
        "status": "Active"
    },
    {
        "screen_id": 260,
        "lesson_id": 39,
        "screen_title": "9",
        "screen_content": "\u0cae\u0cae\u0cbe\u0cae\u0cbf\u0cae\u0cc0\u0cae\u0cc1\u0cae\u0cc2\u0cae\u0cc3\u0cae\u0cc6\u0cae\u0cc7\u0cae\u0cc8\u0cae\u0cca\u0cae\u0ccb\u0cae\u0ccc\u0cae\u0c82\u0cae\u0c83",
        "screen_type": "block",
        "display_order": 9,
        "status": "Active"
    },
    {
        "screen_id": 261,
        "lesson_id": 39,
        "screen_title": "10",
        "screen_content": "\u0cae\u0cae\u0cbe\u0cae\u0cbf\u0cae\u0cc0\u0cae\u0cc1\u0cae\u0cc2\u0cae\u0cc3\u0cae\u0cc6\u0cae\u0cc7\u0cae\u0cc8\u0cae\u0cca\u0cae\u0ccb\u0cae\u0ccc\u0cae\u0c82\u0cae\u0c83\r\n\u0cae\u0cae\u0cbe\u0cae\u0cbf\u0cae\u0cc0\u0cae\u0cc1\u0cae\u0cc2\u0cae\u0cc3\u0cae\u0cc6\u0cae\u0cc7\u0cae\u0cc8\u0cae\u0cca\u0cae\u0ccb\u0cae\u0ccc\u0cae\u0c82\u0cae\u0c83",
        "screen_type": "paragraph",
        "display_order": 10,
        "status": "Active"
    },
    {
        "screen_id": 262,
        "lesson_id": 40,
        "screen_title": "1",
        "screen_content": "\u0caf \u0caf\u0cbe \u0caf\u0cbf \u0caf\u0cc0 \u0caf\u0cc1 \u0caf\u0cc2 \u0caf\u0cc3 \u0caf\u0cc6 \u0caf\u0cc7 \u0caf\u0cc8 \u0caf\u0cca \u0caf\u0ccb \u0caf\u0ccc \u0caf\u0c82 \u0caf\u0c83\r\n\u0cb0 \u0cb0\u0cbe \u0cb0\u0cbf \u0cb0\u0cc0 \u0cb0\u0cc1 \u0cb0\u0cc2 \u0cb0\u0cc3 \u0cb0\u0cc6 \u0cb0\u0cc7 \u0cb0\u0cc8 \u0cb0\u0cca \u0cb0\u0ccb \u0cb0\u0ccc \u0cb0\u0c82 \u0cb0\u0c83\r\n\u0cb2 \u0cb2\u0cbe \u0cb2\u0cbf \u0cb2\u0cc0 \u0cb2\u0cc1 \u0cb2\u0cc2 \u0cb2\u0cc3 \u0cb2\u0cc6 \u0cb2\u0cc7 \u0cb2\u0cc8 \u0cb2\u0cca \u0cb2\u0ccb \u0cb2\u0ccc \u0cb2\u0c82 \u0cb2\u0c83\r\n",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 263,
        "lesson_id": 40,
        "screen_title": "2",
        "screen_content": "\u0cb5 \u0cb5\u0cbe \u0cb5\u0cbf \u0cb5\u0cc0 \u0cb5\u0cc1 \u0cb5\u0cc2 \u0cb5\u0cc3 \u0cb5\u0cc6 \u0cb5\u0cc7 \u0cb5\u0cc8 \u0cb5\u0cca \u0cb5\u0ccb \u0cb5\u0ccc \u0cb5\u0c82 \u0cb5\u0c83\r\n\u0cb6 \u0cb6\u0cbe \u0cb6\u0cbf \u0cb6\u0cc0 \u0cb6\u0cc1 \u0cb6\u0cc2 \u0cb6\u0cc3 \u0cb6\u0cc6 \u0cb6\u0cc7 \u0cb6\u0cc8 \u0cb6\u0cca \u0cb6\u0ccb \u0cb6\u0ccc \u0cb6\u0c82 \u0cb6\u0c83\r\n\u0cb7 \u0cb7\u0cbe \u0cb7\u0cbf \u0cb7\u0cc0 \u0cb7\u0cc1 \u0cb7\u0cc2 \u0cb7\u0cc3 \u0cb7\u0cc6 \u0cb7\u0cc7 \u0cb7\u0cc8 \u0cb7\u0cca \u0cb7\u0ccb \u0cb7\u0ccc \u0cb7\u0c82 \u0cb7\u0c83\r\n",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 264,
        "lesson_id": 40,
        "screen_title": "3",
        "screen_content": "\u0cb8 \u0cb8\u0cbe \u0cb8\u0cbf \u0cb8\u0cc0 \u0cb8\u0cc1 \u0cb8\u0cc2 \u0cb8\u0cc3 \u0cb8\u0cc6 \u0cb8\u0cc7 \u0cb8\u0cc8 \u0cb8\u0cca \u0cb8\u0ccb \u0cb8\u0ccc \u0cb8\u0c82 \u0cb8\u0c83\r\n\u0cb9 \u0cb9\u0cbe \u0cb9\u0cbf \u0cb9\u0cc0 \u0cb9\u0cc1 \u0cb9\u0cc2 \u0cb9\u0cc3 \u0cb9\u0cc6 \u0cb9\u0cc7 \u0cb9\u0cc8 \u0cb9\u0cca \u0cb9\u0ccb \u0cb9\u0ccc \u0cb9\u0c82 \u0cb9\u0c83\r\n\u0cb3 \u0cb3\u0cbe \u0cb3\u0cbf \u0cb3\u0cc0 \u0cb3\u0cc1 \u0cb3\u0cc2 \u0cb3\u0cc3 \u0cb3\u0cc6 \u0cb3\u0cc7 \u0cb3\u0cc8 \u0cb3\u0cca \u0cb3\u0ccb \u0cb3\u0ccc \u0cb3\u0c82 \u0cb3\u0c83\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 265,
        "lesson_id": 40,
        "screen_title": "4",
        "screen_content": "\u0c95\u0ccd\u0cb7 \u0c95\u0ccd\u0cb7\u0cbe \u0c95\u0ccd\u0cb7\u0cbf \u0c95\u0ccd\u0cb7\u0cc0 \u0c95\u0ccd\u0cb7\u0cc1 \u0c95\u0ccd\u0cb7\u0cc2 \u0c95\u0ccd\u0cb7\u0cc3 \u0c95\u0ccd\u0cb7\u0cc6 \u0c95\u0ccd\u0cb7\u0cc7 \u0c95\u0ccd\u0cb7\u0cc8 \u0c95\u0ccd\u0cb7\u0cca \u0c95\u0ccd\u0cb7\u0ccb \u0c95\u0ccd\u0cb7\u0ccc \u0c95\u0ccd\u0cb7\u0c82 \u0c95\u0ccd\u0cb7\u0c83\r\n\u0c9c\u0ccd\u0c9e \u0c9c\u0ccd\u0c9e\u0cbe \u0c9c\u0ccd\u0c9e\u0cbf \u0c9c\u0ccd\u0c9e\u0cc0 \u0c9c\u0ccd\u0c9e\u0cc1 \u0c9c\u0ccd\u0c9e\u0cc2 \u0c9c\u0ccd\u0c9e\u0cc3 \u0c9c\u0ccd\u0c9e\u0cc6 \u0c9c\u0ccd\u0c9e\u0cc7 \u0c9c\u0ccd\u0c9e\u0cc8 \u0c9c\u0ccd\u0c9e\u0cca \u0c9c\u0ccd\u0c9e\u0ccb \u0c9c\u0ccd\u0c9e\u0ccc \u0c9c\u0ccd\u0c9e\u0c82 \u0c9c\u0ccd\u0c9e\u0c83",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 266,
        "lesson_id": 41,
        "screen_title": "1",
        "screen_content": "\u0c95\u0ccd\u0c95\u0c95\u0ccd\u0c95\u0c95\u0ccd\u0c95\u0c95\u0ccd\u0c95\u0c95\u0ccd\u0c95\r\n\u0c96\u0ccd\u0c96\u0c96\u0ccd\u0c96\u0c96\u0ccd\u0c96\u0c96\u0ccd\u0c96\u0c96\u0ccd\u0c96\r\n\u0c97\u0ccd\u0c97\u0c97\u0ccd\u0c97\u0c97\u0ccd\u0c97\u0c97\u0ccd\u0c97\u0c97\u0ccd\u0c97\r\n\u0c98\u0ccd\u0c98\u0c98\u0ccd\u0c98\u0c98\u0ccd\u0c98\u0c98\u0ccd\u0c98\u0c98\u0ccd\u0c98\r\n\u0c99\u0ccd\u0c99\u0c99\u0ccd\u0c99\u0c99\u0ccd\u0c99\u0c99\u0ccd\u0c99\u0c99\u0ccd\u0c99\r\n\u0c95\u0ccd\u0c95\u0c96\u0ccd\u0c96\u0c97\u0ccd\u0c97\u0c98\u0ccd\u0c98\u0c99\u0ccd\u0c99\r\n\u0c99\u0ccd\u0c99\u0c98\u0ccd\u0c98\u0c97\u0ccd\u0c97\u0c96\u0ccd\u0c96\u0c95\u0ccd\u0c95",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 267,
        "lesson_id": 41,
        "screen_title": "2",
        "screen_content": "\u0c9a\u0ccd\u0c9a \u0c9a\u0ccd\u0c9a \u0c9a\u0ccd\u0c9a \u0c9a\u0ccd\u0c9a \u0c9a\u0ccd\u0c9a\r\n\u0c9b\u0ccd\u0c9b \u0c9b\u0ccd\u0c9b \u0c9b\u0ccd\u0c9b \u0c9b\u0ccd\u0c9b \u0c9b\u0ccd\u0c9b\r\n\u0c9c\u0ccd\u0c9c \u0c9c\u0ccd\u0c9c \u0c9c\u0ccd\u0c9c \u0c9c\u0ccd\u0c9c \u0c9c\u0ccd\u0c9c\r\n\u0c9d\u0ccd\u0c9d \u0c9d\u0ccd\u0c9d \u0c9d\u0ccd\u0c9d \u0c9d\u0ccd\u0c9d \u0c9d\u0ccd\u0c9d\r\n\u0c9e\u0ccd\u0c9e \u0c9e\u0ccd\u0c9e \u0c9e\u0ccd\u0c9e \u0c9e\u0ccd\u0c9e \u0c9e\u0ccd\u0c9e\r\n\u0c9a\u0ccd\u0c9a \u0c9b\u0ccd\u0c9b \u0c9c\u0ccd\u0c9c \u0c9d\u0ccd\u0c9d \u0c9e\u0ccd\u0c9e\r\n\u0c9e\u0ccd\u0c9e \u0c9d\u0ccd\u0c9d \u0c9c\u0ccd\u0c9c \u0c9b\u0ccd\u0c9b \u0c9a\u0ccd\u0c9a\r\n",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 268,
        "lesson_id": 41,
        "screen_title": "3",
        "screen_content": "\u0c9f\u0ccd\u0c9f \u0c9f\u0ccd\u0c9f \u0c9f\u0ccd\u0c9f \u0c9f\u0ccd\u0c9f \u0c9f\u0ccd\u0c9f\r\n\u0ca0\u0ccd\u0ca0 \u0ca0\u0ccd\u0ca0 \u0ca0\u0ccd\u0ca0 \u0ca0\u0ccd\u0ca0 \u0ca0\u0ccd\u0ca0\r\n\u0ca1\u0ccd\u0ca1 \u0ca1\u0ccd\u0ca1 \u0ca1\u0ccd\u0ca1 \u0ca1\u0ccd\u0ca1 \u0ca1\u0ccd\u0ca1\r\n\u0ca2\u0ccd\u0ca2 \u0ca2\u0ccd\u0ca2 \u0ca2\u0ccd\u0ca2 \u0ca2\u0ccd\u0ca2 \u0ca2\u0ccd\u0ca2\r\n\u0ca3\u0ccd\u0ca3 \u0ca3\u0ccd\u0ca3 \u0ca3\u0ccd\u0ca3 \u0ca3\u0ccd\u0ca3 \u0ca3\u0ccd\u0ca3\r\n\u0c9f\u0ccd\u0c9f \u0ca0\u0ccd\u0ca0 \u0ca1\u0ccd\u0ca1 \u0ca2\u0ccd\u0ca2 \u0ca3\u0ccd\u0ca3\r\n\u0ca3\u0ccd\u0ca3 \u0ca2\u0ccd\u0ca2 \u0ca1\u0ccd\u0ca1 \u0ca0\u0ccd\u0ca0 \u0c9f\u0ccd\u0c9f\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 269,
        "lesson_id": 41,
        "screen_title": "4",
        "screen_content": "\u0ca4\u0ccd\u0ca4 \u0ca4\u0ccd\u0ca4 \u0ca4\u0ccd\u0ca4 \u0ca4\u0ccd\u0ca4 \u0ca4\u0ccd\u0ca4\r\n\u0ca5\u0ccd\u0ca5 \u0ca5\u0ccd\u0ca5 \u0ca5\u0ccd\u0ca5 \u0ca5\u0ccd\u0ca5 \u0ca5\u0ccd\u0ca5\r\n\u0ca6\u0ccd\u0ca6 \u0ca6\u0ccd\u0ca6 \u0ca6\u0ccd\u0ca6 \u0ca6\u0ccd\u0ca6 \u0ca6\u0ccd\u0ca6\r\n\u0ca7\u0ccd\u0ca7 \u0ca7\u0ccd\u0ca7 \u0ca7\u0ccd\u0ca7 \u0ca7\u0ccd\u0ca7 \u0ca7\u0ccd\u0ca7\r\n\u0ca8\u0ccd\u0ca8 \u0ca8\u0ccd\u0ca8 \u0ca8\u0ccd\u0ca8 \u0ca8\u0ccd\u0ca8 \u0ca8\u0ccd\u0ca8\r\n\u0ca4\u0ccd\u0ca4 \u0ca5\u0ccd\u0ca5 \u0ca6\u0ccd\u0ca6 \u0ca7\u0ccd\u0ca7 \u0ca8\u0ccd\u0ca8\r\n\u0ca8\u0ccd\u0ca8 \u0ca7\u0ccd\u0ca7 \u0ca6\u0ccd\u0ca6 \u0ca5\u0ccd\u0ca5 \u0ca4\u0ccd\u0ca4\r\n",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 270,
        "lesson_id": 41,
        "screen_title": "5",
        "screen_content": "\u0caa\u0ccd\u0caa \u0caa\u0ccd\u0caa \u0caa\u0ccd\u0caa \u0caa\u0ccd\u0caa \u0caa\u0ccd\u0caa\r\n\u0cab\u0ccd\u0cab \u0cab\u0ccd\u0cab \u0cab\u0ccd\u0cab \u0cab\u0ccd\u0cab \u0cab\u0ccd\u0cab\r\n\u0cac\u0ccd\u0cac \u0cac\u0ccd\u0cac \u0cac\u0ccd\u0cac \u0cac\u0ccd\u0cac \u0cac\u0ccd\u0cac\r\n\u0cad\u0ccd\u0cad \u0cad\u0ccd\u0cad \u0cad\u0ccd\u0cad \u0cad\u0ccd\u0cad \u0cad\u0ccd\u0cad\r\n\u0cae\u0ccd\u0cae \u0cae\u0ccd\u0cae \u0cae\u0ccd\u0cae \u0cae\u0ccd\u0cae \u0cae\u0ccd\u0cae\r\n\u0caa\u0ccd\u0caa \u0cab\u0ccd\u0cab \u0cac\u0ccd\u0cac \u0cad\u0ccd\u0cad \u0cae\u0ccd\u0cae\r\n\u0cae\u0ccd\u0cae \u0cad\u0ccd\u0cad \u0cac\u0ccd\u0cac \u0cab\u0ccd\u0cab \u0caa\u0ccd\u0caa",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 271,
        "lesson_id": 41,
        "screen_title": "6",
        "screen_content": "\u0caf\u0ccd\u0caf \u0caf\u0ccd\u0caf \u0caf\u0ccd\u0caf \u0caf\u0ccd\u0caf \u0caf\u0ccd\u0caf\r\n\u0cb0\u0ccd\u0cb0 \u0cb0\u0ccd\u0cb0 \u0cb0\u0ccd\u0cb0 \u0cb0\u0ccd\u0cb0 \u0cb0\u0ccd\u0cb0\r\n\u0cb2\u0ccd\u0cb2 \u0cb2\u0ccd\u0cb2 \u0cb2\u0ccd\u0cb2 \u0cb2\u0ccd\u0cb2 \u0cb2\u0ccd\u0cb2\r\n\u0cb5\u0ccd\u0cb5 \u0cb5\u0ccd\u0cb5 \u0cb5\u0ccd\u0cb5 \u0cb5\u0ccd\u0cb5 \u0cb5\u0ccd\u0cb5\r\n\u0cb6\u0ccd\u0cb6 \u0cb6\u0ccd\u0cb6 \u0cb6\u0ccd\u0cb6 \u0cb6\u0ccd\u0cb6 \u0cb6\u0ccd\u0cb6\r\n\u0cb7\u0ccd\u0cb7 \u0cb7\u0ccd\u0cb7 \u0cb7\u0ccd\u0cb7 \u0cb7\u0ccd\u0cb7 \u0cb7\u0ccd\u0cb7\r\n\u0cb8\u0ccd\u0cb8 \u0cb8\u0ccd\u0cb8 \u0cb8\u0ccd\u0cb8 \u0cb8\u0ccd\u0cb8 \u0cb8\u0ccd\u0cb8\r\n\u0cb9\u0ccd\u0cb9 \u0cb9\u0ccd\u0cb9 \u0cb9\u0ccd\u0cb9 \u0cb9\u0ccd\u0cb9 \u0cb9\u0ccd\u0cb9\r\n\u0cb3\u0ccd\u0cb3 \u0cb3\u0ccd\u0cb3 \u0cb3\u0ccd\u0cb3 \u0cb3\u0ccd\u0cb3 \u0cb3\u0ccd\u0cb3\r\n\u0caf\u0ccd\u0caf \u0cb0\u0ccd\u0cb0 \u0cb2\u0ccd\u0cb2 \u0cb5\u0ccd\u0cb5\r\n\u0cb6\u0ccd\u0cb6 \u0cb7\u0ccd\u0cb7 \u0cb8\u0ccd\u0cb8 \u0cb9\u0ccd\u0cb9 \u0cb3\u0ccd\u0cb3\r\n\u0cb3\u0ccd\u0cb3 \u0cb9\u0ccd\u0cb9 \u0cb8\u0ccd\u0cb8 \u0cb7\u0ccd\u0cb7 \u0cb6\u0ccd\u0cb6\r\n\u0cb5\u0ccd\u0cb5 \u0cb2\u0ccd\u0cb2 \u0cb0\u0ccd\u0cb0 \u0caf\u0ccd\u0caf\r\n",
        "screen_type": "paragraph",
        "display_order": 6,
        "status": "Active"
    },
    {
        "screen_id": 272,
        "lesson_id": 42,
        "screen_title": "1",
        "screen_content": "\u0c95\u0ccd\u0cb0 \u0c96\u0ccd\u0cb0 \u0c97\u0ccd\u0cb0 \u0c98\u0ccd\u0cb0 \u0c99\u0ccd\u0cb0\r\n\u0c9a\u0ccd\u0cb0 \u0c9b\u0ccd\u0cb0 \u0c9c\u0ccd\u0cb0 \u0c9d\u0ccd\u0cb0 \u0c9e\u0ccd\u0cb0\r\n\u0c9f\u0ccd\u0cb0 \u0ca0\u0ccd\u0cb0 \u0ca1\u0ccd\u0cb0 \u0ca2\u0ccd\u0cb0 \u0ca3\u0ccd\u0cb0\r\n\u0ca4\u0ccd\u0cb0 \u0ca5\u0ccd\u0cb0 \u0ca6\u0ccd\u0cb0 \u0ca7\u0ccd\u0cb0 \u0ca8\u0ccd\u0cb0\r\n\u0caa\u0ccd\u0cb0 \u0cab\u0ccd\u0cb0 \u0cac\u0ccd\u0cb0 \u0cad\u0ccd\u0cb0 \u0cae\u0ccd\u0cb0\r\n\u0caf\u0ccd\u0cb0 \u0cb0\u0ccd\u0cb0 \u0cb2\u0ccd\u0cb0 \u0cb5\u0ccd\u0cb0\r\n\u0cb6\u0ccd\u0cb0 \u0cb7\u0ccd\u0cb0 \u0cb8\u0ccd\u0cb0 \u0cb9\u0ccd\u0cb0 \u0cb3\u0ccd\u0cb0",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 273,
        "lesson_id": 42,
        "screen_title": "2",
        "screen_content": "\u0c95\u0ccd\u0caf \u0c96\u0ccd\u0caf \u0c97\u0ccd\u0caf \u0c98\u0ccd\u0caf \u0c99\u0ccd\u0caf\r\n\u0c9a\u0ccd\u0caf \u0c9b\u0ccd\u0caf \u0c9c\u0ccd\u0caf \u0c9d\u0ccd\u0caf \u0c9e\u0ccd\u0caf\r\n\u0c9f\u0ccd\u0caf \u0ca0\u0ccd\u0caf \u0ca1\u0ccd\u0caf \u0ca2\u0ccd\u0caf \u0ca3\u0ccd\u0caf\r\n\u0ca4\u0ccd\u0caf \u0ca5\u0ccd\u0caf \u0ca6\u0ccd\u0caf \u0ca7\u0ccd\u0caf \u0ca8\u0ccd\u0caf\r\n\u0caa\u0ccd\u0caf \u0cab\u0ccd\u0caf \u0cac\u0ccd\u0caf \u0cad\u0ccd\u0caf \u0cae\u0ccd\u0caf\r\n\u0caf\u0ccd\u0caf \u0cb0\u0ccd\u0caf \u0cb2\u0ccd\u0caf \u0cb5\u0ccd\u0caf\r\n\u0cb6\u0ccd\u0caf \u0cb7\u0ccd\u0caf \u0cb8\u0ccd\u0caf \u0cb9\u0ccd\u0caf \u0cb3\u0ccd\u0caf\r\n",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 274,
        "lesson_id": 42,
        "screen_title": "3",
        "screen_content": "\u0c95\u0ccd\u0cb2 \u0c96\u0ccd\u0cb2 \u0c97\u0ccd\u0cb2 \u0c98\u0ccd\u0cb2 \u0c99\u0ccd\u0cb2\r\n\u0c9a\u0ccd\u0cb2 \u0c9b\u0ccd\u0cb2 \u0c9c\u0ccd\u0cb2 \u0c9d\u0ccd\u0cb2 \u0c9e\u0ccd\u0cb2\r\n\u0c9f\u0ccd\u0cb2 \u0ca0\u0ccd\u0cb2 \u0ca1\u0ccd\u0cb2 \u0ca2\u0ccd\u0cb2 \u0ca3\u0ccd\u0cb2\r\n\u0ca4\u0ccd\u0cb2 \u0ca5\u0ccd\u0cb2 \u0ca6\u0ccd\u0cb2 \u0ca7\u0ccd\u0cb2 \u0ca8\u0ccd\u0cb2\r\n\u0caa\u0ccd\u0cb2 \u0cab\u0ccd\u0cb2 \u0cac\u0ccd\u0cb2 \u0cad\u0ccd\u0cb2 \u0cae\u0ccd\u0cb2\r\n\u0caf\u0ccd\u0cb2 \u0cb0\u0ccd\u0cb2 \u0cb2\u0ccd\u0cb2 \u0cb5\u0ccd\u0cb2\r\n\u0cb6\u0ccd\u0cb2 \u0cb7\u0ccd\u0cb2 \u0cb8\u0ccd\u0cb2 \u0cb9\u0ccd\u0cb2 \u0cb3\u0ccd\u0cb2\r\n",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 275,
        "lesson_id": 42,
        "screen_title": "4",
        "screen_content": "\u0c95\u0ccd\u0cb5 \u0c96\u0ccd\u0cb5 \u0c97\u0ccd\u0cb5 \u0c98\u0ccd\u0cb5 \u0c99\u0ccd\u0cb5\r\n\u0c9a\u0ccd\u0cb5 \u0c9b\u0ccd\u0cb5 \u0c9c\u0ccd\u0cb5 \u0c9d\u0ccd\u0cb5 \u0c9e\u0ccd\u0cb5\r\n\u0c9f\u0ccd\u0cb5 \u0ca0\u0ccd\u0cb5 \u0ca1\u0ccd\u0cb5 \u0ca2\u0ccd\u0cb5 \u0ca3\u0ccd\u0cb5\r\n\u0ca4\u0ccd\u0cb5 \u0ca5\u0ccd\u0cb5 \u0ca6\u0ccd\u0cb5 \u0ca7\u0ccd\u0cb5 \u0ca8\u0ccd\u0cb5\r\n\u0caa\u0ccd\u0cb5 \u0cab\u0ccd\u0cb5 \u0cac\u0ccd\u0cb5 \u0cad\u0ccd\u0cb5 \u0cae\u0ccd\u0cb5\r\n\u0caf\u0ccd\u0cb5 \u0cb0\u0ccd\u0cb5 \u0cb2\u0ccd\u0cb5 \u0cb5\u0ccd\u0cb5\r\n\u0cb6\u0ccd\u0cb5 \u0cb7\u0ccd\u0cb5 \u0cb8\u0ccd\u0cb5 \u0cb9\u0ccd\u0cb5 \u0cb3\u0ccd\u0cb5",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 276,
        "lesson_id": 42,
        "screen_title": "5",
        "screen_content": "\u0c95\u0ccd\u0ca8 \u0c96\u0ccd\u0ca8 \u0c97\u0ccd\u0ca8 \u0c98\u0ccd\u0ca8 \u0c99\u0ccd\u0ca8\r\n\u0c9a\u0ccd\u0ca8 \u0c9b\u0ccd\u0ca8 \u0c9c\u0ccd\u0ca8 \u0c9d\u0ccd\u0ca8 \u0c9e\u0ccd\u0ca8\r\n\u0c9f\u0ccd\u0ca8 \u0ca0\u0ccd\u0ca8 \u0ca1\u0ccd\u0ca8 \u0ca2\u0ccd\u0ca8 \u0ca3\u0ccd\u0ca8\r\n\u0ca4\u0ccd\u0ca8 \u0ca5\u0ccd\u0ca8 \u0ca6\u0ccd\u0ca8 \u0ca7\u0ccd\u0ca8 \u0ca8\u0ccd\u0ca8\r\n\u0caa\u0ccd\u0ca8 \u0cab\u0ccd\u0ca8 \u0cac\u0ccd\u0ca8 \u0cad\u0ccd\u0ca8 \u0cae\u0ccd\u0ca8\r\n\u0caf\u0ccd\u0ca8 \u0cb0\u0ccd\u0ca8 \u0cb2\u0ccd\u0ca8 \u0cb5\u0ccd\u0ca8\r\n\u0cb6\u0ccd\u0ca8 \u0cb7\u0ccd\u0ca8 \u0cb8\u0ccd\u0ca8 \u0cb9\u0ccd\u0ca8 \u0cb3\u0ccd\u0ca8",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    },
    {
        "screen_id": 277,
        "lesson_id": 43,
        "screen_title": "1",
        "screen_content": "\u0c85\u0cae\u0ccd\u0cae \u0c85\u0caa\u0ccd\u0caa \u0cae\u0ca8\u0cc6 \u0cae\u0c97\u0cc1 \u0c95\u0cb5\u0cbf \u0cb9\u0cb8\u0cc1 \u0cae\u0cb0 \u0cb9\u0ca3\u0ccd\u0ca3\u0cc1 \r\n\u0cac\u0cc6\u0c82\u0c95\u0cbf \u0cac\u0cc7\u0cb0\u0cc1 \u0c95\u0ca1\u0cc6 \u0cae\u0ca8\u0cc6 \r\n\u0cac\u0c9f\u0ccd\u0c9f\u0cc6 \u0c97\u0cbf\u0ca1 \u0c95\u0cc8 \u0c95\u0cbe\u0cb2\u0cc1 \u0cb9\u0cbe\u0cb2\u0cc1 \u0cb9\u0cc2\u0cb5\u0cc1 \u0ca8\u0cc0\u0cb0\u0cc1 \u0ca6\u0cbe\u0cb0\u0cbf\r\n",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 278,
        "lesson_id": 43,
        "screen_title": "2",
        "screen_content": "\u0c95\u0cb0\u0ca1\u0cbf\r\n\u0cae\u0cb0\u0ca6\r\n\u0c95\u0ca8\u0ccd\u0ca8\u0ca1\r\n\u0cb9\u0cca\u0cb3\u0cc6\u0caf\r\n\u0c97\u0ca3\u0cc7\u0cb6\r\n\u0c85\u0c82\u0c97\u0ca1\u0cbf\r\n\u0c95\u0ca1\u0cb2\u0cc6\r\n\u0cae\u0cbe\u0cb5\u0cbf\u0ca8\r\n\u0c97\u0cc1\u0cb2\u0cbe\u0cac\u0cbf\r\n\u0c9a\u0c82\u0ca6\u0ccd\u0cb0",
        "screen_type": "jump",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 279,
        "lesson_id": 43,
        "screen_title": "3",
        "screen_content": "\u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb0\u0ccd\u0ca5\u0cbf\r\n\u0cb6\u0cbe\u0cb2\u0cc6\r\n\u0c95\u0c82\u0caa\u0ccd\u0caf\u0cc2\u0c9f\u0cb0\u0ccd\r\n\u0caa\u0cc1\u0cb8\u0ccd\u0ca4\u0c95\r\n\u0c85\u0ca7\u0ccd\u0caf\u0cbe\u0caa\u0c95\r\n\u0caa\u0ccd\u0cb0\u0cbe\u0cb0\u0ccd\u0ca5\u0ca8\u0cc6\r\n\u0c86\u0cb8\u0ccd\u0caa\u0ca4\u0ccd\u0cb0\u0cc6\r\n\u0cb5\u0cbf\u0c9c\u0ccd\u0c9e\u0cbe\u0ca8\r\n\u0cb8\u0ccd\u0ca8\u0cc7\u0cb9\u0cbf\u0ca4\r\n\u0caa\u0cb0\u0cc0\u0c95\u0ccd\u0cb7\u0cc6",
        "screen_type": "jump",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 280,
        "lesson_id": 44,
        "screen_title": "1",
        "screen_content": "\u0ca8\u0cbe\u0ca8\u0cc1 \u0cb6\u0cbe\u0cb2\u0cc6\u0c97\u0cc6 \u0cb9\u0ccb\u0c97\u0cc1\u0ca4\u0ccd\u0ca4\u0cc7\u0ca8\u0cc6.\r\n\u0c85\u0cb5\u0ca8\u0cc1 \u0caa\u0cc1\u0cb8\u0ccd\u0ca4\u0c95 \u0c93\u0ca6\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0ca8\u0cc6.\r\n\u0c85\u0cb5\u0cb3\u0cc1 \u0cb9\u0cbe\u0ca1\u0cc1 \u0cb9\u0cbe\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb3\u0cc6.\r\n\u0ca8\u0cbe\u0cb5\u0cc1 \u0c86\u0c9f \u0c86\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cc7\u0cb5\u0cc6.\r\n\u0c87\u0ca6\u0cc1 \u0ca8\u0ca8\u0ccd\u0ca8 \u0cae\u0ca8\u0cc6.\r\n\u0c85\u0ca6\u0cc1 \u0ca6\u0cca\u0ca1\u0ccd\u0ca1 \u0cae\u0cb0.\r\n\u0ca8\u0ca8\u0c97\u0cc6 \u0c95\u0ca8\u0ccd\u0ca8\u0ca1 \u0c87\u0cb7\u0ccd\u0c9f.\r\n\u0c85\u0cae\u0ccd\u0cae \u0c8a\u0c9f \u0cae\u0cbe\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6.\r\n\u0c85\u0caa\u0ccd\u0caa \u0c95\u0cc6\u0cb2\u0cb8\u0c95\u0ccd\u0c95\u0cc6 \u0cb9\u0ccb\u0c97\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6.\r\n\u0ca8\u0cbe\u0caf\u0cbf \u0c9c\u0ccb\u0cb0\u0cbe\u0c97\u0cbf \u0cac\u0cca\u0c97\u0cb3\u0cc1\u0ca4\u0ccd\u0ca4\u0ca6\u0cc6.\r\n",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 281,
        "lesson_id": 44,
        "screen_title": "2",
        "screen_content": "\u0c87\u0c82\u0ca6\u0cc1 \u0cb9\u0cb5\u0cbe\u0cae\u0cbe\u0ca8 \u0c9a\u0cc6\u0ca8\u0ccd\u0ca8\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.\r\n\u0ca8\u0cbe\u0ca8\u0cc1 \u0cac\u0cc6\u0cb3\u0c97\u0ccd\u0c97\u0cc6 \u0cac\u0cc7\u0c97 \u0c8e\u0ca6\u0ccd\u0ca6\u0cc6.\r\n\u0c85\u0cb5\u0cb0\u0cc1 \u0cae\u0cbe\u0cb0\u0cc1\u0c95\u0c9f\u0ccd\u0c9f\u0cc6\u0c97\u0cc6 \u0cb9\u0ccb\u0ca6\u0cb0\u0cc1.\r\n\u0cae\u0c95\u0ccd\u0c95\u0cb3\u0cc1 \u0cb8\u0c82\u0ca4\u0ccb\u0cb7\u0ca6\u0cbf\u0c82\u0ca6 \u0c86\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cbf\u0ca6\u0ccd\u0ca6\u0cbe\u0cb0\u0cc6.\r\n\u0ca8\u0ca8\u0ccd\u0ca8 \u0cb8\u0ccd\u0ca8\u0cc7\u0cb9\u0cbf\u0ca4 \u0c87\u0c82\u0ca6\u0cc1 \u0cac\u0c82\u0ca6\u0ca8\u0cc1.\r\n\u0ca8\u0cbe\u0cb5\u0cc1 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0ca6\u0cbf\u0ca8 \u0c93\u0ca6\u0cc1\u0ca4\u0ccd\u0ca4\u0cc7\u0cb5\u0cc6.\r\n\u0cb6\u0cbf\u0c95\u0ccd\u0cb7\u0c95\u0cb0\u0cc1 \u0c9a\u0cc6\u0ca8\u0ccd\u0ca8\u0cbe\u0c97\u0cbf \u0cac\u0ccb\u0ca7\u0cbf\u0cb8\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6.\r\n\u0ca8\u0ca8\u0c97\u0cc6 \u0caa\u0cc1\u0cb8\u0ccd\u0ca4\u0c95 \u0c93\u0ca6\u0cc1\u0cb5\u0cc1\u0ca6\u0cc1 \u0c87\u0cb7\u0ccd\u0c9f.\r\n\u0cae\u0cb0\u0c97\u0cb3\u0cc1 \u0ca8\u0cae\u0c97\u0cc6 \u0ca8\u0cc6\u0cb0\u0cb3\u0cc1 \u0c95\u0cca\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cb5\u0cc6.\r\n\u0ca8\u0cc0\u0cb0\u0cc1 \u0ca8\u0cae\u0ccd\u0cae \u0c9c\u0cc0\u0cb5\u0ca8\u0c95\u0ccd\u0c95\u0cc6 \u0c85\u0c97\u0ca4\u0ccd\u0caf\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 282,
        "lesson_id": 44,
        "screen_title": "3",
        "screen_content": "\u0ca8\u0cae\u0ccd\u0cae \u0cb6\u0cbe\u0cb2\u0cc6\u0caf\u0cb2\u0ccd\u0cb2\u0cbf \u0c89\u0ca4\u0ccd\u0ca4\u0cae \u0cb6\u0cbf\u0c95\u0ccd\u0cb7\u0c95\u0cb0\u0cbf\u0ca6\u0ccd\u0ca6\u0cbe\u0cb0\u0cc6.\r\n\u0cb5\u0cbf\u0ca6\u0ccd\u0caf\u0cbe\u0cb0\u0ccd\u0ca5\u0cbf\u0c97\u0cb3\u0cc1 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0ca6\u0cbf\u0ca8 \u0cb8\u0cae\u0caf\u0c95\u0ccd\u0c95\u0cc6 \u0cac\u0cb0\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6.\r\n\u0ca8\u0cbe\u0cb5\u0cc1 \u0cb8\u0ccd\u0cb5\u0c9a\u0ccd\u0c9b\u0ca4\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0c95\u0cbe\u0caa\u0cbe\u0ca1\u0cac\u0cc7\u0c95\u0cc1.\r\n\u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0caf\u0cca\u0cac\u0ccd\u0cac\u0cb0\u0cc2 \u0cb6\u0ccd\u0cb0\u0cae\u0ca6\u0cbf\u0c82\u0ca6 \u0caf\u0cb6\u0cb8\u0ccd\u0cb8\u0cc1 \u0caa\u0ca1\u0cc6\u0caf\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6.\r\n\u0c95\u0ca8\u0ccd\u0ca8\u0ca1 \u0ca8\u0cae\u0ccd\u0cae \u0cae\u0cbe\u0ca4\u0cc3\u0cad\u0cbe\u0cb7\u0cc6\u0caf\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.\r\n\u0c85\u0cb5\u0ca8\u0cc1 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0ca6\u0cbf\u0ca8 \u0cb5\u0ccd\u0caf\u0cbe\u0caf\u0cbe\u0cae \u0cae\u0cbe\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0ca8\u0cc6.\r\n\u0caa\u0cc1\u0cb8\u0ccd\u0ca4\u0c95 \u0c9c\u0ccd\u0c9e\u0cbe\u0ca8\u0ca6 \u0c89\u0ca4\u0ccd\u0ca4\u0cae \u0cae\u0cc2\u0cb2\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.\r\n\u0c95\u0ccd\u0cb7\u0cae\u0cc6 \u0c92\u0c82\u0ca6\u0cc1 \u0c89\u0ca4\u0ccd\u0ca4\u0cae \u0c97\u0cc1\u0ca3\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6.\r\n\u0ca8\u0cbe\u0cb5\u0cc1 \u0caa\u0ccd\u0cb0\u0c95\u0cc3\u0ca4\u0cbf\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb0\u0c95\u0ccd\u0cb7\u0cbf\u0cb8\u0cac\u0cc7\u0c95\u0cc1.\r\n\u0cb8\u0ca4\u0ccd\u0caf\u0cb5\u0cc7 \u0c9c\u0caf\u0cbf\u0cb8\u0cc1\u0ca4\u0ccd\u0ca4\u0ca6\u0cc6.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 283,
        "lesson_id": 45,
        "screen_title": "1",
        "screen_content": "\u0ca8\u0ca8\u0ccd\u0ca8 \u0cb6\u0cbe\u0cb2\u0cc6 \u0ca4\u0cc1\u0c82\u0cac\u0cbe \u0cb8\u0cc1\u0c82\u0ca6\u0cb0\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6. \u0ca8\u0cae\u0ccd\u0cae \u0cb6\u0cbe\u0cb2\u0cc6\u0caf\u0cb2\u0ccd\u0cb2\u0cbf \u0c89\u0ca4\u0ccd\u0ca4\u0cae \u0cb6\u0cbf\u0c95\u0ccd\u0cb7\u0c95\u0cb0\u0cbf\u0ca6\u0ccd\u0ca6\u0cbe\u0cb0\u0cc6. \u0c85\u0cb5\u0cb0\u0cc1 \u0ca8\u0cae\u0c97\u0cc6 \u0caa\u0ccd\u0cb0\u0cc0\u0ca4\u0cbf\u0caf\u0cbf\u0c82\u0ca6 \u0caa\u0cbe\u0ca0 \u0cae\u0cbe\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cbe\u0cb0\u0cc6. \u0cb6\u0cbe\u0cb2\u0cc6\u0caf\u0cb2\u0ccd\u0cb2\u0cbf \u0c97\u0ccd\u0cb0\u0c82\u0ca5\u0cbe\u0cb2\u0caf, \u0c86\u0c9f\u0ca6 \u0cae\u0cc8\u0ca6\u0cbe\u0ca8 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c95\u0c82\u0caa\u0ccd\u0caf\u0cc2\u0c9f\u0cb0\u0ccd \u0caa\u0ccd\u0cb0\u0caf\u0ccb\u0c97\u0cbe\u0cb2\u0caf \u0c87\u0ca6\u0cc6. \u0ca8\u0cbe\u0ca8\u0cc1 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0ca6\u0cbf\u0ca8 \u0cb8\u0c82\u0ca4\u0ccb\u0cb7\u0ca6\u0cbf\u0c82\u0ca6 \u0cb6\u0cbe\u0cb2\u0cc6\u0c97\u0cc6 \u0cb9\u0ccb\u0c97\u0cc1\u0ca4\u0ccd\u0ca4\u0cc7\u0ca8\u0cc6.",
        "screen_type": "paragraph",
        "display_order": 1,
        "status": "Active"
    },
    {
        "screen_id": 284,
        "lesson_id": 45,
        "screen_title": "2",
        "screen_content": "\u0cae\u0cb0\u0c97\u0cb3\u0cc1 \u0ca8\u0cae\u0ccd\u0cae \u0c9c\u0cc0\u0cb5\u0ca8\u0ca6 \u0c85\u0cae\u0cc2\u0cb2\u0ccd\u0caf \u0cb8\u0c82\u0caa\u0ca4\u0ccd\u0ca4\u0cbe\u0c97\u0cbf\u0cb5\u0cc6. \u0c85\u0cb5\u0cc1 \u0ca8\u0cae\u0c97\u0cc6 \u0cb6\u0cc1\u0ca6\u0ccd\u0ca7 \u0c97\u0cbe\u0cb3\u0cbf, \u0ca8\u0cc6\u0cb0\u0cb3\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cae\u0cb3\u0cc6\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0ca8\u0cc0\u0ca1\u0cc1\u0ca4\u0ccd\u0ca4\u0cb5\u0cc6. \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0caf\u0cca\u0cac\u0ccd\u0cac\u0cb0\u0cc2 \u0ca4\u0cae\u0ccd\u0cae \u0c9c\u0cc0\u0cb5\u0ca8\u0ca6\u0cb2\u0ccd\u0cb2\u0cbf \u0c95\u0ca8\u0cbf\u0cb7\u0ccd\u0ca0 \u0c92\u0c82\u0ca6\u0cc1 \u0cae\u0cb0\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0ca8\u0cc6\u0ca1\u0cac\u0cc7\u0c95\u0cc1. \u0caa\u0cb0\u0cbf\u0cb8\u0cb0\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0ccd\u0cb5\u0c9a\u0ccd\u0c9b\u0cb5\u0cbe\u0c97\u0cbf\u0c9f\u0ccd\u0c9f\u0cb0\u0cc6 \u0ca8\u0cae\u0ccd\u0cae \u0c86\u0cb0\u0ccb\u0c97\u0ccd\u0caf\u0cb5\u0cc2 \u0c89\u0ca4\u0ccd\u0ca4\u0cae\u0cb5\u0cbe\u0c97\u0cbf\u0cb0\u0cc1\u0ca4\u0ccd\u0ca4\u0ca6\u0cc6.",
        "screen_type": "paragraph",
        "display_order": 2,
        "status": "Active"
    },
    {
        "screen_id": 285,
        "lesson_id": 45,
        "screen_title": "3",
        "screen_content": "\u0c95\u0ca8\u0ccd\u0ca8\u0ca1\u0cb5\u0cc1 \u0ca8\u0cae\u0ccd\u0cae \u0ca8\u0cbe\u0ca1\u0cbf\u0ca8 \u0cb9\u0cc6\u0cae\u0ccd\u0cae\u0cc6\u0caf \u0cad\u0cbe\u0cb7\u0cc6\u0caf\u0cbe\u0c97\u0cbf\u0ca6\u0cc6. \u0c87\u0ca6\u0cc1 \u0cb6\u0ccd\u0cb0\u0cc0\u0cae\u0c82\u0ca4 \u0cb8\u0cbe\u0cb9\u0cbf\u0ca4\u0ccd\u0caf \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cb8\u0c82\u0cb8\u0ccd\u0c95\u0cc3\u0ca4\u0cbf\u0caf\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb9\u0cca\u0c82\u0ca6\u0cbf\u0ca6\u0cc6. \u0c95\u0ca8\u0ccd\u0ca8\u0ca1\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cae\u0cbe\u0ca4\u0ca8\u0cbe\u0ca1\u0cc1\u0cb5\u0cc1\u0ca6\u0cc1, \u0c93\u0ca6\u0cc1\u0cb5\u0cc1\u0ca6\u0cc1 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cac\u0cb0\u0cc6\u0caf\u0cc1\u0cb5\u0cc1\u0ca6\u0cc1 \u0caa\u0ccd\u0cb0\u0ca4\u0cbf\u0caf\u0cca\u0cac\u0ccd\u0cac \u0c95\u0ca8\u0ccd\u0ca8\u0ca1\u0cbf\u0c97\u0ca8 \u0c9c\u0cb5\u0cbe\u0cac\u0ccd\u0ca6\u0cbe\u0cb0\u0cbf\u0caf\u0cbe\u0c97\u0cbf\u0ca6\u0cc6. \u0ca8\u0cbe\u0cb5\u0cc1 \u0c8e\u0cb2\u0ccd\u0cb2\u0cc6\u0ca1\u0cc6 \u0c95\u0ca8\u0ccd\u0ca8\u0ca1\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c97\u0ccc\u0cb0\u0cb5\u0ca6\u0cbf\u0c82\u0ca6 \u0cac\u0cb3\u0cb8\u0cac\u0cc7\u0c95\u0cc1.",
        "screen_type": "paragraph",
        "display_order": 3,
        "status": "Active"
    },
    {
        "screen_id": 286,
        "lesson_id": 45,
        "screen_title": "4",
        "screen_content": "\u0c87\u0c82\u0ca6\u0cbf\u0ca8 \u0c9c\u0cc0\u0cb5\u0ca8\u0ca6\u0cb2\u0ccd\u0cb2\u0cbf \u0ca4\u0c82\u0ca4\u0ccd\u0cb0\u0c9c\u0ccd\u0c9e\u0cbe\u0ca8\u0c95\u0ccd\u0c95\u0cc6 \u0cae\u0cb9\u0ca4\u0ccd\u0cb5\u0ca6 \u0cb8\u0ccd\u0ca5\u0cbe\u0ca8\u0cb5\u0cbf\u0ca6\u0cc6. \u0c95\u0c82\u0caa\u0ccd\u0caf\u0cc2\u0c9f\u0cb0\u0ccd \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c87\u0c82\u0c9f\u0cb0\u0ccd\u0ca8\u0cc6\u0c9f\u0ccd \u0ca8\u0cae\u0ccd\u0cae \u0c95\u0cc6\u0cb2\u0cb8\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0cc1\u0cb2\u0cad\u0c97\u0cca\u0cb3\u0cbf\u0cb8\u0cbf\u0cb5\u0cc6. \u0cb9\u0cca\u0cb8 \u0ca4\u0c82\u0ca4\u0ccd\u0cb0\u0c9c\u0ccd\u0c9e\u0cbe\u0ca8\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb8\u0cb0\u0cbf\u0caf\u0cbe\u0ca6 \u0cb0\u0cc0\u0ca4\u0cbf\u0caf\u0cb2\u0ccd\u0cb2\u0cbf \u0cac\u0cb3\u0cb8\u0cbf\u0ca6\u0cb0\u0cc6 \u0c9c\u0ccd\u0c9e\u0cbe\u0ca8 \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0c95\u0ccc\u0cb6\u0cb2\u0ccd\u0caf\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0cb9\u0cc6\u0c9a\u0ccd\u0c9a\u0cbf\u0cb8\u0cbf\u0c95\u0cca\u0cb3\u0ccd\u0cb3\u0cac\u0cb9\u0cc1\u0ca6\u0cc1. \u0ca4\u0c82\u0ca4\u0ccd\u0cb0\u0c9c\u0ccd\u0c9e\u0cbe\u0ca8\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c9c\u0cb5\u0cbe\u0cac\u0ccd\u0ca6\u0cbe\u0cb0\u0cbf\u0caf\u0cbf\u0c82\u0ca6 \u0cac\u0cb3\u0cb8\u0cc1\u0cb5\u0cc1\u0ca6\u0cc1 \u0c85\u0ca4\u0ccd\u0caf\u0c97\u0ca4\u0ccd\u0caf.",
        "screen_type": "paragraph",
        "display_order": 4,
        "status": "Active"
    },
    {
        "screen_id": 287,
        "lesson_id": 45,
        "screen_title": "5",
        "screen_content": "\u0caa\u0cb0\u0cbf\u0cb6\u0ccd\u0cb0\u0cae\u0cb5\u0cc1 \u0caf\u0cb6\u0cb8\u0ccd\u0cb8\u0cbf\u0ca8 \u0cae\u0cc2\u0cb2\u0cb5\u0cbe\u0c97\u0cbf\u0ca6\u0cc6. \u0caf\u0cbe\u0cb5\u0cc1\u0ca6\u0cc7 \u0c95\u0cc6\u0cb2\u0cb8\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0caa\u0ccd\u0cb0\u0cbe\u0cae\u0cbe\u0ca3\u0cbf\u0c95\u0cb5\u0cbe\u0c97\u0cbf \u0cae\u0ca4\u0ccd\u0ca4\u0cc1 \u0cb6\u0ccd\u0cb0\u0ca6\u0ccd\u0ca7\u0cc6\u0caf\u0cbf\u0c82\u0ca6 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0cb0\u0cc6 \u0c89\u0ca4\u0ccd\u0ca4\u0cae \u0cab\u0cb2\u0cbf\u0ca4\u0cbe\u0c82\u0cb6 \u0ca6\u0cca\u0cb0\u0cc6\u0caf\u0cc1\u0ca4\u0ccd\u0ca4\u0ca6\u0cc6. \u0cb8\u0cae\u0caf\u0cb5\u0ca8\u0ccd\u0ca8\u0cc1 \u0c97\u0ccc\u0cb0\u0cb5\u0cbf\u0cb8\u0cbf \u0ca8\u0cbf\u0cb0\u0c82\u0ca4\u0cb0 \u0c85\u0cad\u0ccd\u0caf\u0cbe\u0cb8 \u0cae\u0cbe\u0ca1\u0cbf\u0ca6\u0cb0\u0cc6 \u0c9c\u0cc0\u0cb5\u0ca8\u0ca6\u0cb2\u0ccd\u0cb2\u0cbf \u0caf\u0cb6\u0cb8\u0ccd\u0cb8\u0cc1 \u0cb8\u0cbe\u0ca7\u0cbf\u0cb8\u0cac\u0cb9\u0cc1\u0ca6\u0cc1. \u0caa\u0cb0\u0cbf\u0cb6\u0ccd\u0cb0\u0cae\u0c95\u0ccd\u0c95\u0cc6 \u0caf\u0cbe\u0cb5\u0ca4\u0ccd\u0ca4\u0cc2 \u0caa\u0cb0\u0ccd\u0caf\u0cbe\u0caf\u0cb5\u0cbf\u0cb2\u0ccd\u0cb2.",
        "screen_type": "paragraph",
        "display_order": 5,
        "status": "Active"
    }
]

TYPING_GAMES_DATA = [
    {
        "game_id": 1,
        "game_name": "Jump Ball",
        "category": "Speed",
        "difficulty": "Medium",
        "status": "Active"
    }
]

def seed_lms_data():
    """
    Idempotently seeds LMS content into the database.
    Checks for existing records before inserting to avoid duplicates.
    """
    inserted_courses = 0
    inserted_lessons = 0
    inserted_screens = 0
    inserted_games = 0

    # Seed Courses
    for c_data in COURSES_DATA:
        existing = db.session.get(Course, c_data['course_id'])
        if not existing:
            course = Course(
                course_id=c_data['course_id'],
                course_name=c_data['course_name'],
                status=c_data.get('status', 'Active')
            )
            db.session.add(course)
            inserted_courses += 1

    if inserted_courses > 0:
        db.session.commit()

    # Seed Lessons
    for l_data in LESSONS_DATA:
        existing = db.session.get(Lesson, l_data['lesson_id'])
        if not existing:
            lesson = Lesson(
                lesson_id=l_data['lesson_id'],
                course_id=l_data['course_id'],
                lesson_title=l_data['lesson_title'],
                lesson_description=l_data.get('lesson_description'),
                chapter=l_data.get('chapter', 'Beginner'),
                display_order=l_data.get('display_order', 1),
                status=l_data.get('status', 'Active')
            )
            db.session.add(lesson)
            inserted_lessons += 1

    if inserted_lessons > 0:
        db.session.commit()

    # Seed Screens
    for s_data in SCREENS_DATA:
        existing = db.session.get(Screen, s_data['screen_id'])
        if not existing:
            screen = Screen(
                screen_id=s_data['screen_id'],
                lesson_id=s_data['lesson_id'],
                screen_title=s_data['screen_title'],
                screen_content=s_data['screen_content'],
                screen_type=s_data.get('screen_type', 'block'),
                display_order=s_data.get('display_order', 1),
                status=s_data.get('status', 'Active')
            )
            db.session.add(screen)
            inserted_screens += 1

    if inserted_screens > 0:
        db.session.commit()

    # Seed Typing Games
    for g_data in TYPING_GAMES_DATA:
        existing = db.session.get(TypingGame, g_data['game_id'])
        if not existing:
            game = TypingGame(
                game_id=g_data['game_id'],
                game_name=g_data['game_name'],
                category=g_data.get('category', 'Speed & Accuracy'),
                difficulty=g_data.get('difficulty', 'Medium'),
                status=g_data.get('status', 'Active')
            )
            db.session.add(game)
            inserted_games += 1

    if inserted_games > 0:
        db.session.commit()

    if inserted_courses + inserted_lessons + inserted_screens + inserted_games > 0:
        print(f"[LMS Seed] Seeding complete: {inserted_courses} courses, {inserted_lessons} lessons, {inserted_screens} screens, {inserted_games} games inserted.")
    else:
        print("[LMS Seed] LMS content already present. Skipping seed.")

def export_lms_to_seed_file():
    """
    Exports LMS content from local SQLite database (instance/typing.db) into seed_lms.py.
    """
    import sqlite3
    import json
    import os

    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'typing.db')
    if not os.path.exists(db_path):
        print(f"[LMS Seed Export] Error: Database file not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    courses = [dict(r) for r in cur.execute('SELECT course_id, course_name, status FROM courses ORDER BY course_id').fetchall()]
    lessons = [dict(r) for r in cur.execute('SELECT lesson_id, course_id, lesson_title, lesson_description, chapter, display_order, status FROM lessons ORDER BY lesson_id').fetchall()]
    screens = [dict(r) for r in cur.execute('SELECT screen_id, lesson_id, screen_title, screen_content, screen_type, display_order, status FROM lesson_screens ORDER BY screen_id').fetchall()]
    games = [dict(r) for r in cur.execute('SELECT game_id, game_name, category, difficulty, status FROM typing_games ORDER BY game_id').fetchall()]

    current_file = os.path.abspath(__file__)
    with open(current_file, 'r', encoding='utf-8') as f:
        full_code = f.read()

    seed_func_marker = "def seed_lms_data():"
    idx = full_code.find(seed_func_marker)
    if idx == -1:
        print("[LMS Seed Export] Error: Could not find seed_lms_data function in file.")
        return

    func_and_tail = full_code[idx:]

    header = '''"""
LMS Production Seeding System.
Contains seed data exported from local SQLite database (courses, lessons, lesson_screens, typing_games).
Preserves exact primary keys and foreign key relationships.
"""

import sys
from database import db
from models import Course, Lesson, Screen, TypingGame
'''
    new_content = header + f"\nCOURSES_DATA = {json.dumps(courses, indent=4)}\n\nLESSONS_DATA = {json.dumps(lessons, indent=4)}\n\nSCREENS_DATA = {json.dumps(screens, indent=4)}\n\nTYPING_GAMES_DATA = {json.dumps(games, indent=4)}\n\n" + func_and_tail

    with open(current_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"[LMS Seed Export] Exported {len(courses)} courses, {len(lessons)} lessons, {len(screens)} screens, {len(games)} games into {current_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_lms_to_seed_file()
    else:
        from app import app
        with app.app_context():
            seed_lms_data()
