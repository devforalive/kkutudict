#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def load_words(filename):
    """단어 목록을 파일에서 읽어온다"""
    with open(filename, 'r', encoding='utf-8') as f:
        words = [word.strip() for word in f.readlines() if word.strip()]
    return words

def find_words_by_first_char(words, first_char):
    """첫 글자로 시작하는 단어들을 찾는다"""
    return [word for word in words if word.startswith(first_char)]

def main():
    # 단어 목록 읽기
    words = load_words('word_list.txt')
    print(f"총 {len(words)}개의 단어를 읽었습니다.\n")
    
    while True:
        user_input = input("찾을 글자를 입력하세요 (종료: 'q'): ").strip()
        
        if user_input.lower() == 'q':
            print("프로그램을 종료합니다.")
            break
        
        if not user_input:
            print("글자를 입력해주세요.\n")
            continue
        
        # 첫 번째 글자만 사용
        first_char = user_input[0]
        
        # 단어 찾기
        found_words = find_words_by_first_char(words, first_char)
        
        if found_words:
            print(f"\n'{first_char}'로 시작하는 단어 ({len(found_words)}개):")
            for i, word in enumerate(found_words, 1):
                print(f"  {i}. {word}")
            print()
        else:
            print(f"\n'{first_char}'로 시작하는 단어가 없습니다.\n")

if __name__ == '__main__':
    main()
