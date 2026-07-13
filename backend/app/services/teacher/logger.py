from __future__ import annotations




class TeacherLogger:
    # ==========================================================
    # Teacher Brain
    # ==========================================================

    def brain(
        self,
        brain_state,
    ):
        perception = brain_state.perception
        reflection = brain_state.reflection
        
        plan = brain_state.planning
        lesson = brain_state.lesson

        print()
        print("=" * 60)
        print("TEACHER BRAIN 2.0")
        print("=" * 60)

        # ------------------------------------------------------
        # PERCEPTION
        # ------------------------------------------------------

        print()
        print("PERCEPTION")
        print("-" * 60)

        print(f"HAS ERROR:            {perception.has_error}")
        print(f"DETECTED SKILL:       {perception.detected_skill}")
        print(f"TARGET SKILL:         {perception.target_skill}")
        print(f"CURRENT FOCUS:        {perception.current_focus}")
        print(f"ESTIMATED LEVEL:      {perception.estimated_level}")
        print(f"STUDENT CONFIDENT:    {perception.student_confident}")
        print(f"NEEDS INTERVENTION:   {perception.needs_intervention}")

        # ------------------------------------------------------
        # REFLECTION
        # ------------------------------------------------------

        print()
        print("REFLECTION")
        print("-" * 60)

        print(f"CONTINUE LESSON:      {reflection.should_continue_lesson}")
        print(f"START NEW LESSON:     {reflection.should_start_new_lesson}")
        print(f"REVIEW:               {reflection.should_review}")
        print(f"REASON:               {reflection.teaching_reason}")
        print(
        f"INTERRUPTION LEVEL:   {reflection.interruption_level}"
        )
       


        # ------------------------------------------------------
        # PLANNING
        # ------------------------------------------------------

        print()
        print("PLANNING")
        print("-" * 60)

        print(f"GOAL:                 {plan.goal}")
        print(f"LESSON TYPE:          {plan.lesson_type}")
        print(f"TEACHING PRIORITY:    {plan.teaching_priority}")
        print(f"INTERRUPTION:         {plan.interruption_level}")
        print(f"CONVERSATION:         {plan.conversation_policy}")
        print(f"TARGET SKILL:         {plan.target_skill}")
        print(f"EXPLANATION LEVEL:    {plan.explanation_level}")
        print(f"REQUIRES EXERCISE:    {plan.requires_exercise}")
        print(f"REQUIRES REVIEW:      {plan.requires_review}")


        # ------------------------------------------------------
        # ACTION PLAN
        # ------------------------------------------------------

        print()
        print("ACTION PLAN")
        print("-" * 60)

        print(f"GOAL:                 {plan.goal}")

        print(f"LESSON TYPE:          {plan.lesson_type}")

        print(f"TARGET SKILL:         {plan.target_skill}")

        print()

        print(f"MODE:                 {plan.teaching_mode}")

        print(f"ACTION:               {plan.action}")

        print(f"REASON:               {plan.teacher_reason}")

        print()

        print(f"STYLE:                {plan.response_style}")

        print(f"TONE:                 {plan.tone}")

        print(f"EXPLANATION:          {plan.explanation_level}")

        print()

        print(f"GENERATE EXAMPLE:     {plan.generate_example}")

        print(f"GENERATE EXERCISE:    {plan.generate_exercise}")

        print(f"ASK QUESTION:         {plan.ask_question}")

        print(f"WAIT STUDENT:         {plan.wait_for_student}")

        print(f"FINISH LESSON:        {plan.finish_lesson}")

        print()

        print(f"SHOULD TEACH:         {plan.should_teach}")

        print(f"SHOULD REVIEW:        {plan.should_review}")

        print(f"SHOULD EXERCISE:      {plan.should_exercise}")

        print()

        print(f"CONFIDENCE:           {plan.confidence:.2f}")

        print(f"PRIORITY:             {plan.teaching_priority}")

        # ------------------------------------------------------
        # LESSON STATE
        # ------------------------------------------------------

        print()
        print("LESSON STATE")
        print("-" * 60)

        print(f"ACTIVE:               {lesson.active}")
        print(f"GOAL:                 {lesson.goal}")
        print(f"LESSON TYPE:          {lesson.lesson_type}")
        print(f"TARGET SKILL:         {lesson.target_skill}")
        print(f"CURRENT PHASE:        {lesson.current_phase}")
        print(f"STEP:                 {lesson.current_step} / {lesson.total_steps}")
        print(f"EXPECTED TURNS:       {lesson.expected_turns}")
        print(f"TURNS ELAPSED:        {lesson.turns_elapsed}")
        print(f"LAST ACTION:          {lesson.last_teacher_action}")
        print(f"COMPLETED:            {lesson.completed}")

        print("=" * 60)

        

    # ==========================================================
    # Teacher Decision
    # ==========================================================

    def decision(
        self,
        teacher_decision,
    ):

        print()
        print("=" * 60)
        print("TEACHER DECISION")
        print("=" * 60)

        print(
            f"INTENT:        {teacher_decision.intent.value}"
        )

        print(
            f"PRIORITY:      {teacher_decision.priority}"
        )

        print(
            f"CONFIDENCE:    {teacher_decision.confidence:.2f}"
        )

        print("=" * 60)


teacher_logger = TeacherLogger()
