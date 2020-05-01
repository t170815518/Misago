import { Trans } from "@lingui/macro"
import React from "react"
import { Link } from "react-router-dom"
import { Icon } from "../../../UI"
import * as urls from "../../../urls"

interface IThreadsStartButtonProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsStartButton: React.FC<IThreadsStartButtonProps> = ({
  category,
}) => (
  <Link className="btn btn-primary" to={urls.startThread(category)}>
    <Icon icon="edit" fixedWidth />
    <span>
      <Trans id="btn.new-thread">New thread</Trans>
    </span>
  </Link>
)

export default ThreadsStartButton