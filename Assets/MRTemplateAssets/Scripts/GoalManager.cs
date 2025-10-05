using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine.InputSystem;
using UnityEngine.UI;
using UnityEngine.XR.Interaction.Toolkit.Samples.StarterAssets;
using TMPro;
using LazyFollow = UnityEngine.XR.Interaction.Toolkit.UI.LazyFollow;
using UnityEngine.XR.ARFoundation;

namespace UnityEngine.XR.Templates.MR
{
    public static class aparecerCardapio
    {
        public static bool aparecer = true;
    }
    public struct Goal
    {
        public GoalManager.OnboardingGoals CurrentGoal;
        public bool Completed;

        public Goal(GoalManager.OnboardingGoals goal)
        {
            CurrentGoal = goal;
            Completed = false;
        }
    }

    public class GoalManager : MonoBehaviour
    {
        public enum OnboardingGoals
        {
            pagina1,
            pagina2,
        }

        Queue<Goal> m_OnboardingGoals;
        Goal m_CurrentGoal;
        bool m_AllGoalsFinished;
        int m_SurfacesTapped;
        int m_CurrentGoalIndex = 0;
        public InputActionProperty recordButton;
        [Serializable]
        class Step
        {
            [SerializeField]
            public GameObject stepObject;

            [SerializeField]
            public string buttonText;

        }

        [SerializeField]
        public LazyFollow m_GoalPanelLazyFollow;

        [SerializeField]
        List<Step> m_StepList = new List<Step>();

        [SerializeField]
        public TextMeshProUGUI m_StepButtonTextField;

        [SerializeField]
        ObjectSpawner m_ObjectSpawner;

        const int k_NumberOfSurfacesTappedToCompleteGoal = 1;
        Vector3 m_TargetOffset = new Vector3(-.5f, -.25f, 1.5f);

        void Start()
        {
            m_OnboardingGoals = new Queue<Goal>();
            var P1 = new Goal(OnboardingGoals.pagina1);
            var P2 = new Goal(OnboardingGoals.pagina2);

            m_OnboardingGoals.Enqueue(P1);
            m_OnboardingGoals.Enqueue(P2);

            m_CurrentGoal = m_OnboardingGoals.Dequeue();

        }

        void Update()
        {
            if (!m_AllGoalsFinished)
            {
                ProcessGoals();
            }

            // Debug Input
#if UNITY_EDITOR
            if (Keyboard.current.spaceKey.wasPressedThisFrame)
            {
                CompleteGoal();
            }
#endif
        }
        void OnEnable()
        {
            recordButton.action.Enable();
            recordButton.action.performed += OnRecordButtonPressed;
        }

        void OnDisable()
        {
            recordButton.action.performed -= OnRecordButtonPressed;
            recordButton.action.Disable();
        }

        void OnRecordButtonPressed(InputAction.CallbackContext ctx)
        {
            // Alterna visibilidade da janela
            bool novaVisibilidade = !m_GoalPanelLazyFollow.gameObject.activeSelf;
            m_GoalPanelLazyFollow.gameObject.SetActive(novaVisibilidade);

            // Alterna gravação de voz
            var gravador = Object.FindAnyObjectByType<GravacaoDeVoz>();
            if (gravador != null)
            {
                gravador.AlterarGravacao(ctx);
            }
        }

        void ProcessGoals()
        {
            if (!m_CurrentGoal.Completed)
            {
                m_GoalPanelLazyFollow.positionFollowMode = LazyFollow.PositionFollowMode.Follow;
            }
        }

        public void CompleteGoal()
        {
            m_CurrentGoal.Completed = true;
            m_CurrentGoalIndex++;
            if (m_OnboardingGoals.Count > 0)
            {
                m_CurrentGoal = m_OnboardingGoals.Dequeue();
                m_StepList[m_CurrentGoalIndex - 1].stepObject.SetActive(false);
                m_StepList[m_CurrentGoalIndex].stepObject.SetActive(true);
                m_StepButtonTextField.text = m_StepList[m_CurrentGoalIndex].buttonText;
            }
            else
            {
                ResetCoaching();

            }
        }

        public void ResetCoaching()
        {

            m_OnboardingGoals.Clear();
            m_OnboardingGoals = new Queue<Goal>();
            var P1 = new Goal(OnboardingGoals.pagina1);
            var P2 = new Goal(OnboardingGoals.pagina2);

            m_OnboardingGoals.Enqueue(P1);
            m_OnboardingGoals.Enqueue(P2);

            for (int i = 0; i < m_StepList.Count; i++)
            {
                if (i == 0)
                {
                    m_StepList[i].stepObject.SetActive(true);
                    m_StepButtonTextField.text = m_StepList[i].buttonText;
                }
                else
                {
                    m_StepList[i].stepObject.SetActive(false);
                }
            }

            m_CurrentGoal = m_OnboardingGoals.Dequeue();
            m_AllGoalsFinished = false;

            m_CurrentGoalIndex = 0;
        }
    }
}
