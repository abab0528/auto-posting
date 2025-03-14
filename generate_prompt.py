def generate_prompt(style_description, topic, audience, length, keywords, format_choice):
    # 글 길이에 맞는 문구 추가
    if length == "short":
        length_instruction = "글 길이는 500자 이하로 간결하게 작성해주세요."
    elif length == "long":
        length_instruction = "글 길이는 1000자 이상으로 충분히 상세하게 작성해주세요."
    else:
        length_instruction = "글 길이는 중간 정도로 작성해주세요."

    # 포스팅 형식에 맞는 문구 추가
    if format_choice == "list":
        format_instruction = "리스트 형식으로 각 항목을 간결하게 나열해주세요."
    elif format_choice == "essay":
        format_instruction = "에세이 형식으로 감성적으로 풀어주세요."
    else:
        format_instruction = "블로그 포스팅 형식으로 작성해 주세요."

    # 키워드가 있을 경우 키워드 강조
    if keywords:
        keywords_instruction = f"이 글에는 다음의 키워드를 포함해 주세요: {keywords}"
    else:
        keywords_instruction = "특별히 포함된 키워드는 없습니다."

    #독자층 반영
    audience_instruction = f"이 글의 대상 독자는 {audience} 입니다."

    # 최종 프롬프트
    combined_prompt = f"""
    다음 스타일 설명을 바탕으로 주어진 주제에 맞는 블로그 글을 작성해 주세요. 스타일을 그대로 반영해서 작성하세요:

    스타일 설명:
    {style_description}

    주제: {topic}

    {length_instruction}
    {keywords_instruction}
    {format_instruction}
    {audience_instruction}

    작성한 글의 내용은 사용자가 입력한 주제와 요구사항을 반영해주세요.
    """

    return combined_prompt    
