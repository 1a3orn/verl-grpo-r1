set -x

export VLLM_ATTENTION_BACKEND=XFORMERS

python3 -m verl.trainer.main_grpo \
    algorithm.adv_estimator=grpo \
    data.train_files=$DATA_DIR/all_zebralogic_train.parquet \
    data.val_files=[$DATA_DIR/all_geography_test.parquet,$DATA_DIR/all_gsm8k_test.parquet,$DATA_DIR/all_trash_math_test.parquet,$DATA_DIR/all_zebralogic_test.parquet] \
    data.train_batch_size=6 \
    data.val_batch_size=6 \
    data.max_prompt_length=512 \
    data.max_response_length=3500 \
    actor_rollout_ref.model.path="./models/Qwen2.5-3B-Instruct" \
    actor_rollout_ref.actor.optim.lr=4e-6 \
    actor_rollout_ref.model.use_remove_padding=True \
    actor_rollout_ref.actor.ppo_mini_batch_size=25 \
    actor_rollout_ref.actor.ppo_micro_batch_size_per_gpu=3 \
    actor_rollout_ref.actor.use_kl_loss=True \
    actor_rollout_ref.actor.kl_loss_coef=0.008 \
    actor_rollout_ref.actor.kl_loss_type=low_var_kl \
    actor_rollout_ref.model.enable_gradient_checkpointing=True \
    actor_rollout_ref.actor.fsdp_config.param_offload=False \
    actor_rollout_ref.actor.fsdp_config.grad_offload=False \
    actor_rollout_ref.actor.fsdp_config.optimizer_offload=False \
    actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=20 \
    actor_rollout_ref.rollout.tensor_model_parallel_size=2 \
    actor_rollout_ref.rollout.name=vllm \
    actor_rollout_ref.rollout.gpu_memory_utilization=0.3 \
    actor_rollout_ref.rollout.n=16 \
    actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=3 \
    actor_rollout_ref.ref.fsdp_config.param_offload=True \
    algorithm.kl_ctrl.kl_coef=0.001 \
    critic.ppo_micro_batch_size=3 \
    critic.ppo_mini_batch_size=3 \
    trainer.critic_warmup=0 \
    trainer.logger=['console','wandb'] \
    trainer.project_name="grpo_generalization_2" \
    trainer.experiment_name="train_zebralogic_02" \
    trainer.n_gpus_per_node=2 \
    trainer.nnodes=1 \
    trainer.save_freq=-1 \
    trainer.test_freq=50 \
    trainer.total_epochs=15 2>&1 | tee verl_demo.log