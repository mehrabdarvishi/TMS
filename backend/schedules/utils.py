def overlapping_sessions_wrapped(sessions):
    result = []
    height = 0
    for i in range(len(sessions)-1):
        overlap_found = False
        for j in range(i+1, len(sessions)):
            session_1, session_2 = sessions[i], sessions[j]
            if session_1.start_time <= session_2.end_time and session_1.end_time >= session_2.start_time:
                result.append([session_1, session_2])
                overlap_found = True
        if not overlap_found:
            result.append(session_1)
    return result

